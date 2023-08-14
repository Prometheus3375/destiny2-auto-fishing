from threading import Thread
from time import sleep

from .configurator import ConfigParameter, Configurable
from .methods.base import BaseMethod


def _ask_input():
    _ = input('Press Enter to exit\n')


class Fisher(Configurable, config_group=''):
    """
    Main class for fishing.
    """
    __slots__ = 'fishing_method', 'fish_limit', 'do_initial_cast'

    def __init__(
            self,
            fishing_method: BaseMethod,
            /,
            fish_limit: float = 50,
            do_initial_cast: bool = True,
            ):
        """
        :param fishing_method: a method of fishing which used
          to cast the fishing rod and catch fish.
        :param fish_limit: the maximum number of fish to catch.
          Defaults to 50.
        :param do_initial_cast: whether to immediately cast the fishing rod
          when fishing loop starts.
          Defaults to ``True``.
        """
        assert isinstance(fishing_method, BaseMethod)
        assert isinstance(fish_limit, (int, float)) and fish_limit > 0
        assert isinstance(do_initial_cast, bool)

        self.fishing_method = fishing_method
        self.fish_limit = fish_limit
        self.do_initial_cast = do_initial_cast

    def start(self, /):
        """
        Starts fishing.
        """
        fish_count = 0
        try:
            print('Switch to Destiny 2 window. Ensure it is active while script is running')

            for time in range(5, 0, -1):
                print(f'Starting in {time}s', end='\r')
                sleep(1)

            thread = Thread(target=_ask_input, daemon=True)
            thread.start()

            anti_afk = self.fishing_method.anti_afk
            # Loop anti-afk only if fish limit is reached
            loop_anti_afk = False

            for b in self.fishing_method.start(self.do_initial_cast):
                fish_count += b
                if fish_count >= self.fish_limit:
                    print('Fish limit is reached; collect it and restart the script')
                    loop_anti_afk = anti_afk is not None
                    break
                elif not thread.is_alive():
                    print('Enter is pressed')
                    break

            if loop_anti_afk:
                print('Anti AFK is enabled; the script continues to run until terminated manually')
                for _ in anti_afk.loop_actions():
                    if not thread.is_alive():
                        print('Enter is pressed')
                        break

        except KeyboardInterrupt:
            print('Ctrl+C is pressed')

        print(f'Script is terminated. {fish_count} fish caught')

    @staticmethod
    def config_parameters() -> list[ConfigParameter]:
        excluded_params = {'fishing_method'}

        enable_anti_afk_doc = 'Whether to enable anti-AFK actions. Defaults to ``True``.'
        return [
            *(
                cp
                for cp in ConfigParameter.function_params(Fisher.__init__)
                if cp.name not in excluded_params
                ),
            ConfigParameter('enable_anti_afk', bool, enable_anti_afk_doc, True),
            ]


__all__ = 'Fisher',
