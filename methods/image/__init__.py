from collections.abc import Iterator
from time import sleep

from PIL import ImageGrab

from .functions import *
from ..base import BaseMethod


# Ideal catch button stays for 12 frames in 30 FPS video,
# but there are only 3 frames where interact button is solid.
# Thus, minimal screen grab period should be at least 0.05.


class ImageMethod(BaseMethod):
    """
    Fishing method which uses screen capture to detect an opportunity of fish catch.

    :param bbox_x0: screen X coordinate where capturing bounding box starts.
    :param bbox_y0: screen Y coordinate where capturing bounding box starts.
    :param key_image_path: path to a sample image in PGN format of the interaction key.
    :param tolerance: how far average values can be from the desired ones.
    :param screen_grap_period: time in seconds how often screen should be captured.
      Defaults to 1/30.
    :param kwargs: refer to :class:`BaseMethod` for additional settings.
    """
    __slots__ = 'key_matrix', 'tolerance', 'bbox', 'screen_grap_period'

    def __init__(
            self,
            /,
            bbox_x0: int,
            bbox_y0: int,
            key_image_path: str,
            tolerance: int,
            screen_grap_period: float = 1 / 30,
            **kwargs,
            ):
        super().__init__(**kwargs)

        assert isinstance(bbox_x0, int) and bbox_x0 >= 0
        assert isinstance(bbox_y0, int) and bbox_y0 >= 0
        assert isinstance(key_image_path, str) and len(key_image_path) > 0
        assert isinstance(tolerance, int) and tolerance >= 1
        assert isinstance(screen_grap_period, (int, float)) and screen_grap_period > 0

        with open_image(key_image_path) as im:
            self.key_matrix = image_matrix(im)
            x, y = self.key_matrix.shape

        self.tolerance = tolerance
        self.bbox = (bbox_x0, bbox_y0, bbox_x0 + x, bbox_y0 + y)
        self.screen_grap_period = screen_grap_period

    @classmethod
    def from_predefined(
            cls,
            /,
            screen_width: int,
            screen_height: int,
            localization: str,
            key: str,
            **kwargs,
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

        loc = available_localizations.get(f'{localization.lower()}_{resolution}')
        k = available_keys.get(f'{key.lower()}_{resolution}')

        if not loc and not k:
            raise ValueError(
                f'cannot find predefined localization {localization!r} '
                f'and key {key!r} for screen resolution {resolution}'
                )

        if not loc:
            raise ValueError(
                f'cannot find predefined localization {localization!r} '
                f'for screen resolution {resolution}'
                )

        if not k:
            raise ValueError(
                f'cannot find predefined key {key!r} '
                f'for screen resolution {resolution}'
                )

        return cls(
            bbox_x0=loc.bbox_x0,
            bbox_y0=loc.bbox_y0,
            interact_key=k.name,
            key_image_path=k.image_path,
            tolerance=k.tolerance,
            **kwargs,
            )

    def _start(self, /) -> Iterator[bool]:
        while True:
            # Image grab takes up to 0.04 seconds on 1920x1080
            diff = difference_matrix_image(self.key_matrix, ImageGrab.grab(self.bbox))
            do_catch: bool = (diff <= self.tolerance).all()

            self._debug(f'Difference: {diff!r}', f'Do catch: {do_catch}')

            yield do_catch
            sleep(self.screen_grap_period)


__all__ = 'ImageMethod',
