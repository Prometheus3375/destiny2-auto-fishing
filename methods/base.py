from collections.abc import Iterator
from datetime import datetime
from time import sleep

from pyautogui import keyDown, keyUp


# After catch there are ~100 frames in 30 FPS video before interact button appears again.
# Interact button should be held for ~11 frames to continue fishing.


class BaseMethod:
    """
    Base method for all fishing methods.

    :param interact_key: a key that is used to catch fish and cast fishing rod.
      Defaults to `e`.
    :param delay_after_catch: time in seconds to wait after catch before casting fishing rod.
      Defaults to 3.34.
    :param cast_duration: time in seconds to hold interact key to cast fishing rod.
      Defaults to 0.5.
    :param debug_file_path: a path to debug log file.
      This file is used to write debug information.
      Defaults to ``None`` which means no debug file.
    """
    __slots__ = (
        'interact_key',
        'delay_after_catch',
        'cast_duration',
        'debug_file',
        )

    def __init__(
            self,
            /,
            interact_key: str = 'e',
            delay_after_catch: float = 3.34,
            cast_duration: float = 0.5,
            debug_file_path: str = None,
            ):
        assert isinstance(interact_key, str) and len(interact_key) > 0
        assert isinstance(delay_after_catch, (int, float)) and delay_after_catch > 0
        assert isinstance(cast_duration, (int, float)) and cast_duration > 0
        assert debug_file_path is None or (isinstance(debug_file_path, str) and debug_file_path)

        self.interact_key = interact_key
        self.delay_after_catch = delay_after_catch
        self.cast_duration = cast_duration
        self.debug_file = debug_file_path

    def _debug(self, /, *lines: str):
        """
        If there is a file for debug log, opens it and appends passed strings.
        Every string is prepended with the current datetime and appended with line feed.
        """
        if self.debug_file:
            dt = datetime.now()
            dt = dt.replace(microsecond=round(dt.microsecond, -3))
            with open(self.debug_file, 'a', encoding='utf-8') as f:
                for line in lines:
                    f.write(f'{dt} {line}\n')

    def cast(self, /):
        """
        Issues a command to cast fishing rod.
        """
        keyDown(self.interact_key)
        sleep(self.cast_duration)
        keyUp(self.interact_key)

    def catch(self, /):
        """
        Issues a command to catch fish.
        """
        keyDown(self.interact_key)
        keyUp(self.interact_key)

    def _start(self, /):
        """
        Starts an infinite loop of fishing.
        If fish can be successfully caught, yields ``True``.
        Yields ``False`` in any other case.
        """
        raise NotImplementedError

    def start(self, do_cast: bool, /) -> Iterator[bool]:
        """
        Starts an infinite loop of fishing.
        If fish is successfully caught, yields ``True``.
        Yields ``False`` in any other case.

        :param do_cast: if ``True``, then casts fishing rod before entering the loop.
        """
        if do_cast:
            self.cast()
            yield False

        for do_catch in self._start():
            if do_catch:
                self.catch()
                yield True
                sleep(self.delay_after_catch)
                yield False
                self.cast()

            yield False
