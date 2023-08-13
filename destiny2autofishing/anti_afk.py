from collections.abc import Iterator
from time import perf_counter, sleep

from .controls import press_key


class AntiAFK:
    """
    A system to perform anti-AFK actions.

    Currently, the actions are the following:

    #. Press ``F1``.
    #. Wait 1 second.
    #. Press ``D``.
    #. Wait 1 second.
    #. Press ``F1``.
    """
    __slots__ = (
        'action_period',
        'no_cast_threshold',
        '_last_time_actions_done',
        '_last_time_rod_cast',
        )

    def __init__(
            self,
            /,
            action_period: int = 120,
            no_cast_threshold: int = 150,
            ):
        """
        :param action_period: time in seconds how often anti-AFK actions should be done.
          Defaults to 120, value must be in range ``[30, 300]``.
        :param no_cast_threshold: time in seconds. If so much time passes since the last cast
          of the fishing rod, then the system will perform anti-AFK actions
          as soon as possible, without waiting for the cast.
          Defaults to 90, value must be in range ``[30, 300]``.
        """
        assert isinstance(action_period, int) and 30 <= action_period <= 300
        assert isinstance(no_cast_threshold, int) and \
               30 <= no_cast_threshold <= 300

        self.action_period = action_period
        self.no_cast_threshold = no_cast_threshold
        self._last_time_actions_done = self._last_time_rod_cast = perf_counter()

    def act(self, current_time: float, /):
        """
        Takes the current time in seconds and
        if anti-AFK actions were performed ``action_period`` seconds or more ago, performs them.
        Otherwise, does nothing.
        """
        if current_time - self._last_time_actions_done >= self.action_period:
            self._last_time_actions_done = current_time
            press_key('f1')
            sleep(1)
            press_key('d')
            sleep(1)
            press_key('f1')

    def act_based_on_catch(self, rod_cast: bool, /):
        """
        Takes a boolean indicating whether the fishing rod is cast or not.
        If the rod is cast or the last cast was ``no_cast_threshold`` seconds or more ago,
        then calls method ``act``. Otherwise, does nothing.
        """
        current_time = perf_counter()
        if rod_cast:
            self._last_time_rod_cast = current_time

        if rod_cast or current_time - self._last_time_rod_cast >= self.no_cast_threshold:
            self.act(current_time)

    def loop_actions(self, /) -> Iterator[None]:
        """
        Starts an infinite loop of calling method ``act`` every second.
        After each call ``None`` is yielded.
        """
        while True:
            self.act(perf_counter())
            yield None
            sleep(1)


__all__ = 'AntiAFK',
