import os
from collections.abc import Iterator
from time import perf_counter, sleep
from timeit import default_timer

from PIL.ImageGrab import grab

from .functions import *
from ..base import BaseMethod
from ...configurator import ConfigParameter
from ...functions import current_datetime_ms_str


class ImageMethod(BaseMethod, name='image'):
    """
    Fishing method which uses screen capture to detect an opportunity of fish catch.
    """
    __slots__ = 'key_matrix', 'tolerance', 'bbox', 'screen_grap_period', 'image_debug_path'

    def __init__(
            self,
            /,
            bbox_x0: int,
            bbox_y0: int,
            key_image_path: str,
            tolerance: int,
            screen_grab_period: float = 1 / 30,
            # Ideal catch button stays for 12 frames in 30 FPS video,
            # but there are only 3 frames where interact button is solid.
            # Thus, minimal screen grab period should be at least 0.05.
            image_debug_path: str = '',
            **kwargs,
            ):
        """
        :param bbox_x0: Screen X coordinate where capturing bounding box starts.
        :param bbox_y0: Screen Y coordinate where capturing bounding box starts.
        :param key_image_path: Path to a sample image in PNG format of the interaction key.
        :param tolerance: How far captured pixel values can differ from
          the pixel values of the image at ``key_image_path`` to trigger fish catch.
        :param screen_grab_period: Time in seconds how often screen should be captured.
          **Note**: screen capturing take much time and
          this time is different for different screen resolutions.
          For example, for screen 1920x1080 it takes ~0.032 seconds to take a screenshot.
          Thus, the actual period can be higher than this value.
          Defaults to 1/30.
        :param image_debug_path: Path to a directory where captured images are stored for debug.
          Images are saved only after catching a fish.
          Defaults to the empty string which means no debug directory.

        Any additionally passed keyword arguments are passed to :class:`BaseMethod` constructor.
        """
        assert isinstance(bbox_x0, int) and bbox_x0 >= 0
        assert isinstance(bbox_y0, int) and bbox_y0 >= 0
        assert isinstance(key_image_path, str) and key_image_path
        assert isinstance(tolerance, int) and tolerance >= 0
        assert isinstance(screen_grab_period, (int, float)) and screen_grab_period >= 0
        assert isinstance(image_debug_path, str)

        super().__init__(**kwargs)

        with open_image(key_image_path) as im:
            self.key_matrix = image_matrix(im)
            x, y = self.key_matrix.shape

        self.tolerance = tolerance
        self.bbox = (bbox_x0, bbox_y0, bbox_x0 + x, bbox_y0 + y)
        self.screen_grap_period = screen_grab_period
        self.image_debug_path = image_debug_path
        if image_debug_path:
            os.makedirs(image_debug_path, exist_ok=True)

    def _start(self, /) -> Iterator[bool]:
        while True:
            secs = perf_counter()
            img = grab(self.bbox)
            diff = difference_matrix_image(self.key_matrix, img)
            do_catch = diff <= self.tolerance

            yield do_catch
            self._log('Difference: {0}; do catch: {1}', diff, do_catch)
            if self.image_debug_path and do_catch:
                # Colons are not allowed in file names
                dt = current_datetime_ms_str().replace(':', '-')
                img.save(f'{self.image_debug_path}/{diff:03} {dt}.png')

            delay = secs + self.screen_grap_period - default_timer()
            if delay > 0: sleep(delay)

    @staticmethod
    def config_parameters() -> list[ConfigParameter]:
        return ConfigParameter.function_params(ImageMethod.__init__)


__all__ = 'ImageMethod',
