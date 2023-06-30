from collections.abc import Iterator
from datetime import datetime
from time import sleep

from pyautogui import keyDown, keyUp


# After hook there are ~100 frames in 30 FPS video before interact button appears again.
# Interact button should be held for ~11 frames to continue fishing.


class BaseMethod:
    __slots__ = (
        'interact_key',
        'hook_duration',
        'delay_after_hook',
        'cast_duration',
        'debug_file',
        )

    def __init__(
            self,
            /,
            interact_key: str = 'e',
            hook_duration: float = 0.1,
            delay_after_hook: float = 3.3,
            cast_duration: float = 0.5,
            debug_file_path: str = None,
            ):
        """
        :param interact_key: a key that is used to hook fish and cast fishing rod.
          Defaults to `e`.
        :param hook_duration: time in seconds to hold interact key to hook fish.
          Defaults to 0.1.
        :param delay_after_hook: time in seconds to wait after hook before casting fishing rod.
          Defaults to 3.5.
        :param cast_duration: time in seconds to hold interact key to cast fishing rod.
          Defaults to 0.5.
        :param debug_file_path: a path to debug log file.
          This file is used to write debug information.
          Defaults to ``None`` which means no debug file.
        """
        assert isinstance(interact_key, str) and len(interact_key) > 0
        assert isinstance(hook_duration, (int, float)) and hook_duration > 0
        assert isinstance(delay_after_hook, (int, float)) and delay_after_hook > 0
        assert isinstance(cast_duration, (int, float)) and cast_duration > 0
        assert debug_file_path is None or (isinstance(debug_file_path, str) and debug_file_path)

        self.interact_key = interact_key
        self.hook_duration = hook_duration
        self.delay_after_hook = delay_after_hook
        self.cast_duration = cast_duration
        self.debug_file = debug_file_path

    def _debug(self, /, *lines: str):
        """
        If there is a file for debug log, opens it and appends passed strings.
        Every string is prepended with the current datetime and appended with line feed.
        """
        if self.debug_file:
            dt = datetime.now().replace(microsecond=0)
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

    def hook(self, /):
        """
        Issues a command to hook fish.
        """
        keyDown(self.interact_key)
        sleep(self.hook_duration)
        keyUp(self.interact_key)

    def _start(self, /):
        """
        Starts an infinite loop of fishing.
        If fish can be successfully hooked, yields ``True``.
        Yields ``False`` in any other case.
        """
        raise NotImplementedError

    def start(self, do_cast: bool, /) -> Iterator[bool]:
        """
        Starts an infinite loop of fishing.
        If fish is successfully hooked, yields ``True``.
        Yields ``False`` in any other case.

        :param do_cast: if ``True``, then casts fishing rod before entering the loop.
        """
        if do_cast:
            self.cast()
            yield False

        for do_hook in self._start():
            if do_hook:
                self.hook()
                yield True
                sleep(self.delay_after_hook)
                yield False
                self.cast()

            yield False
