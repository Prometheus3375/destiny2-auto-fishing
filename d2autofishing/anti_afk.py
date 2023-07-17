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
    #. Press ``ESC``.

    :param action_period: time in seconds how often anti-AFK actions should be done.
      Defaults to 120, minimum value is 30.
    :param no_fish_threshold: time in seconds for how long no fish can be caught.
      After this threshold is passed, the system will continue to perform anti-AFK actions
      despite stopped fishing.
      Defaults to 60, minimum value is 30.
    """
    __slots__ = (
        'action_period',
        'no_fish_threshold',
        '_last_time_fish_caught',
        '_last_time_action_done',
        )

    def __init__(
            self,
            /,
            action_period: float = 120,
            no_fish_threshold: float = 60,
            ):
        assert isinstance(action_period, (float, int)) and action_period >= 30
        assert isinstance(no_fish_threshold, (float, int)) and no_fish_threshold >= 30

        self.action_period = action_period
        self.no_fish_threshold = no_fish_threshold
        self._last_time_fish_caught = self._last_time_action_done = perf_counter()

    def act(self, current_time: float, /):
        """
        Takes the current time in seconds and
        if anti-AFK actions were performed a period or more ago, performs them.
        Otherwise, does nothing.
        """
        if current_time - self._last_time_action_done >= self.action_period:
            self._last_time_action_done = current_time
            press_key('f1')
            sleep(1)
            press_key('d')
            sleep(1)
            press_key('esc')

    def act_based_on_catch(self, fish_caught: bool, /):
        """
        Takes a boolean indicating whether fish was caught or not.
        If fish was caught, or the last catch was ``no_fish_threshold`` seconds or more ago,
        then calls method ``act``. Otherwise, does nothing.
        """
        current_time = perf_counter()
        if fish_caught:
            self._last_time_fish_caught = current_time

        if fish_caught or current_time - self._last_time_fish_caught >= self.no_fish_threshold:
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
