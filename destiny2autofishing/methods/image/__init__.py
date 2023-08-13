import os
from collections.abc import Iterator
from time import perf_counter, sleep
from timeit import default_timer

from PIL.ImageGrab import grab

from .functions import *
from ..base import BaseMethod
from ...functions import current_datetime_ms_str


# Ideal catch button stays for 12 frames in 30 FPS video,
# but there are only 3 frames where interact button is solid.
# Thus, minimal screen grab period should be at least 0.05.


class ImageMethod(BaseMethod):
    """
    Fishing method which uses screen capture to detect an opportunity of fish catch.

    :param bbox_x0: screen X coordinate where capturing bounding box starts.
    :param bbox_y0: screen Y coordinate where capturing bounding box starts.
    :param key_image_path: path to a sample image in PNG format of the interaction key.
    :param tolerance: how far pixel values can be from the desired ones.
    :param screen_grab_period: time in seconds how often screen should be captured.
      **Note**: screen capturing take much time and
      this time is different for different screen resolutions.
      For example, for screen 1920x1080 it takes ~0.032 seconds to take a screenshot.
      Thus, the actual period can be higher than this value.
      Defaults to 1/30.
    :param: image_debug_path: path to a directory where captured images are stored for debug.
      Images are saved only after catching a fish.
      Defaults to the empty string which means no debug directory.
    :param kwargs: refer to :class:`BaseMethod` for additional settings.
    """
    name = 'image'

    __slots__ = 'key_matrix', 'tolerance', 'bbox', 'screen_grap_period', 'image_debug_path'

    def __init__(
            self,
            /,
            bbox_x0: int,
            bbox_y0: int,
            key_image_path: str,
            tolerance: int,
            screen_grab_period: float = 1 / 30,
            image_debug_path: str = '',
            **kwargs,
            ):
        super().__init__(**kwargs)

        assert isinstance(bbox_x0, int) and bbox_x0 >= 0
        assert isinstance(bbox_y0, int) and bbox_y0 >= 0
        assert isinstance(key_image_path, str) and key_image_path
        assert isinstance(tolerance, int) and tolerance >= 0
        assert isinstance(screen_grab_period, (int, float)) and screen_grab_period >= 0
        assert isinstance(image_debug_path, str)

        with open_image(key_image_path) as im:
            self.key_matrix = image_matrix(im)
            x, y = self.key_matrix.shape

        self.tolerance = tolerance
        self.bbox = (bbox_x0, bbox_y0, bbox_x0 + x, bbox_y0 + y)
        self.screen_grap_period = screen_grab_period
        self.image_debug_path = image_debug_path
        if image_debug_path:
            os.makedirs(image_debug_path, exist_ok=True)

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
            is_mouse_button=k.is_mouse_button,
            key_image_path=k.image_path,
            tolerance=k.tolerance,
            **kwargs,
            )

    def _start(self, /) -> Iterator[bool]:
        while True:
            secs = perf_counter()
            img = grab(self.bbox)
            diff = difference_matrix_image(self.key_matrix, img)
            do_catch = diff <= self.tolerance

            yield do_catch
            self._log('Difference: {0}; do catch: {1}', diff, do_catch)
            if self.image_debug_path and do_catch:
                # colons are not allowed in file names
                dt = current_datetime_ms_str().replace(':', '-')
                img.save(f'{self.image_debug_path}/{diff:03} {dt}.png')

            delay = secs + self.screen_grap_period - default_timer()
            if delay > 0: sleep(delay)


__all__ = 'ImageMethod',
