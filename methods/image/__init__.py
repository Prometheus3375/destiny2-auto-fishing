from collections.abc import Iterator
from time import sleep

from PIL import ImageGrab
from numpy import asarray, ndarray

from .functions import calculate_averages
from ..base import BaseMethod


# Ideal catch button stays for 12 frames in 30 FPS video,
# but there are only 3 frames where interact button is solid.
# Thus, minimal screen grab period should be at least 0.05.


class ImageMethod(BaseMethod):
    """
    Fishing method which uses screen capture to detect an opportunity of fish catch.

    :param bbox_x0: screen X coordinate where capturing bounding box starts.
    :param bbox_y0: screen Y coordinate where capturing bounding box starts.
    :param x_averages: desired average values over X axis
      for captured images to issue catch command.
    :param y_averages: desired average values over Y
      for captured images to issue catch command.
    :param tolerance: how far average values can be from the desired ones.
    :param screen_grap_period: time in seconds how often screen should be captured.
      Defaults to 0.04.
    :param kwargs: refer to :class:`BaseMethod` for additional settings.
    """
    __slots__ = (
        'x_averages',
        'y_averages',
        'tolerance',
        'bbox',
        'screen_grap_period',
        )

    def __init__(
            self,
            /,
            bbox_x0: int,
            bbox_y0: int,
            x_averages: list[int],
            y_averages: list[int],
            tolerance: int,
            screen_grap_period: float = 0.04,
            **kwargs,
            ):
        super().__init__(**kwargs)

        assert isinstance(bbox_x0, int) and bbox_x0 >= 0
        assert isinstance(bbox_y0, int) and bbox_y0 >= 0
        assert isinstance(x_averages, list)
        assert isinstance(y_averages, list)
        bbox_x_length = len(x_averages)
        bbox_y_length = len(y_averages)
        assert bbox_x_length > 0
        assert bbox_y_length > 0
        assert all(isinstance(v, int) and 0 <= v <= 255 for v in x_averages)
        assert all(isinstance(v, int) and 0 <= v <= 255 for v in y_averages)
        assert isinstance(tolerance, int) and tolerance >= 1

        self.x_averages = asarray(x_averages, int)
        self.y_averages = asarray(y_averages, int)
        self.tolerance = tolerance
        self.bbox = (bbox_x0, bbox_y0, bbox_x0 + bbox_x_length, bbox_y0 + bbox_y_length)

        assert isinstance(screen_grap_period, (int, float)) and screen_grap_period > 0

        self.screen_grap_period = screen_grap_period

    @classmethod
    def from_predefined(
            cls,
            /,
            screen_width: int,
            screen_height: int,
            localization: str,
            key: str,
            ):
        """
        Creates :class`ImageMethod` from predefined settings.
        """
        assert isinstance(screen_width, int) and screen_width > 0
        assert isinstance(screen_height, int) and screen_height > 0
        assert isinstance(localization, str) and len(localization) > 0
        assert isinstance(key, str) and len(key) > 0

        from predefined.image import available_keys, available_localizations

        resolution = f'{screen_width}x{screen_height}'

        localizations = available_localizations.get(f'{localization.lower()}_{resolution}')
        keys = available_keys.get(f'{key.lower()}_{resolution}')

        if not localizations and not keys:
            raise ValueError(
                f'cannot find predefined localization {localization!r} '
                f'and key {key!r} for screen resolution {resolution}'
                )

        if not localizations:
            raise ValueError(
                f'cannot find predefined localization {localization!r} '
                f'for screen resolution {resolution}'
                )

        if not keys:
            raise ValueError(
                f'cannot find predefined key {key!r} '
                f'for screen resolution {resolution}'
                )

        return cls(
            bbox_x0=localizations.bbox_x0,
            bbox_y0=localizations.bbox_y0,
            interact_key=keys.name,
            x_averages=keys.x_averages,
            y_averages=keys.y_averages,
            tolerance=keys.tolerance,
            )

    def _start(self, /) -> Iterator[bool]:
        while True:
            image = ImageGrab.grab(self.bbox)
            avg_x, avg_y = calculate_averages(image)
            diff_x: ndarray = abs(avg_x - self.x_averages)
            diff_y: ndarray = abs(avg_y - self.y_averages)
            do_catch = (diff_x <= self.tolerance).all() and (diff_y <= self.tolerance).all()

            self._debug(
                f'X difference {diff_x!r}',
                f'Y difference {diff_y!r}',
                f'Do catch: {do_catch}',
                )

            yield do_catch
            sleep(self.screen_grap_period)


__all__ = 'ImageMethod',
