import os
from collections.abc import Iterator
from time import sleep

from ..anti_afk import AntiAFK
from ..controls import *
from ..functions import current_datetime_ms_str, current_datetime_str


# After catch there are ~100 frames in 30 FPS video before interact button appears again.
# Interact button should be held for ~11 frames to continue fishing.


class BaseMethod:
    """
    Base method for all fishing methods.

    :param interact_key: a key that is used to catch fish and cast the fishing rod.
      Defaults to ``e``.
    :param is_mouse_button: should be ``True`` if ``interact_key`` is a mouse button.
      Defaults to ``False``.
    :param delay_after_catch: time in seconds to wait after catch before casting the fishing rod.
      Defaults to 3.3.
    :param cast_duration: time in seconds to hold interact key to cast the fishing rod.
      Defaults to 1.
    :param log_directory_path: path to a directory where log files will be stored.
      Log file is used to write debug information, its name is the current date and time.
      Defaults to ``None`` which means no log directory and no current log file.
    :param anti_afk: an instance of :class:`AntiAFK` or ``None``.
      This instance is used to perform actions preventing the game considering the player as AFK.
      If ``None``, then anti-AFK is disabled.
      Defaults to ``None``.
    """
    __slots__ = (
        '_press',
        '_hold',
        '_interact_key',
        'delay_after_catch',
        'cast_duration',
        'log_file',
        'anti_afk',
        )

    def __init__(
            self,
            /,
            interact_key: str = 'e',
            is_mouse_button: bool = False,
            delay_after_catch: float = 3.3,
            cast_duration: float = 1,  # 0.6 is not enough at low FPS
            anti_afk: AntiAFK | None = None,
            log_directory_path: str | None = None,
            ):
        assert isinstance(interact_key, str) and interact_key
        assert isinstance(is_mouse_button, bool)
        assert isinstance(delay_after_catch, (int, float)) and delay_after_catch > 0
        assert isinstance(cast_duration, (int, float)) and cast_duration > 0
        assert anti_afk is None or isinstance(anti_afk, AntiAFK)
        assert log_directory_path is None or \
               (isinstance(log_directory_path, str) and log_directory_path)

        self._interact_key = interact_key
        self._press = press_mouse if is_mouse_button else press_key
        self._hold = hold_mouse if is_mouse_button else hold_key

        self.delay_after_catch = delay_after_catch
        self.cast_duration = cast_duration
        self.anti_afk = anti_afk

        if log_directory_path:
            os.makedirs(log_directory_path, exist_ok=True)
            self.log_file = os.path.join(
                log_directory_path,
                current_datetime_str().replace(':', '-'),
                )
        else:
            self.log_file = None

    def _log(self, line: str, /, *args, **kwargs):
        """
        If there is a file for logs, opens it and appends passed string with format arguments.
        The result is prepended with the current datetime and appended with line feed.
        """
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f'{current_datetime_ms_str()}    {line.format(*args, *kwargs)}\n')

    def cast(self, /):
        """
        Issues a command to cast the fishing rod.
        """
        self._hold(self._interact_key, self.cast_duration)

    def catch(self, /):
        """
        Issues a command to catch fish.
        """
        self._press(self._interact_key)

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

        :param do_cast: if ``True``, then casts the fishing rod before entering the loop.
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

            if self.anti_afk: self.anti_afk.act_based_on_catch(do_catch)
            yield False
