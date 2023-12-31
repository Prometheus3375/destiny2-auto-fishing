from threading import Thread
from time import sleep

from .anti_afk import AntiAFK
from .configurator import Config, ConfigParameter, Configurable
from .methods.base import BaseMethod


def _ask_input():
    try:
        _ = input('Press Enter to exit\n')
    except EOFError:
        pass


class Fisher(Configurable, config_group=''):
    """
    Main class for fishing.
    """
    __slots__ = 'anti_afk', 'fishing_method', 'fish_limit', 'do_initial_cast'

    def __init__(
            self,
            fishing_method: BaseMethod,
            anti_afk: AntiAFK | None,
            /,
            fish_limit: float = 50,
            do_initial_cast: bool = True,
            ):
        """
        :param fishing_method: A method of fishing which used
          to cast the fishing rod and catch fish.
        :param anti_afk: An instance of :class:`AntiAFK` or ``None``.
          This instance is used to perform actions preventing the game to consider a player as AFK.
          If ``None``, then anti-AFK actions are not performed.
        :param fish_limit: The maximum number of fish to catch.
          People reported that fish can disappear if there is ~60 uncollected fish.
          Put ``inf`` to disable this limit.
          Defaults to 50.
        :param do_initial_cast: Whether to cast the fishing rod at the start.
          Defaults to ``True``.
        """
        assert isinstance(fishing_method, BaseMethod)
        assert anti_afk is None or isinstance(anti_afk, AntiAFK)
        assert isinstance(fish_limit, (int, float)) and fish_limit > 0
        assert isinstance(do_initial_cast, bool)

        self.fishing_method = fishing_method
        self.anti_afk = anti_afk
        fishing_method.anti_afk = anti_afk

        self.fish_limit = fish_limit
        self.do_initial_cast = do_initial_cast

    def start(self, /):
        """
        Starts fishing.
        """
        fish_count = 0
        try:
            print(f'Fish limit is set to {self.fish_limit}')
            print('Anti-AFK is enabled' if self.anti_afk else 'Anti-AFK is disabled')
            print(f'Using fishing method {self.fishing_method.name!r}')
            print('\nSwitch to Destiny 2 window. Ensure it is active while script is running')

            for time in range(5, 0, -1):
                print(f'Starting in {time}s', end='\r')
                sleep(1)

            thread = Thread(target=_ask_input, daemon=True)
            thread.start()

            # Loop anti-afk only if fish limit is reached
            loop_anti_afk = False

            for b in self.fishing_method.start(self.do_initial_cast):
                fish_count += b
                if fish_count >= self.fish_limit:
                    print('Fish limit is reached; collect it and restart the script')
                    loop_anti_afk = self.anti_afk is not None
                    break
                elif not thread.is_alive():
                    print('Enter is pressed')
                    break

            if loop_anti_afk:
                print('Anti-AFK is enabled; the script continues to run until terminated manually')
                for _ in self.anti_afk.loop_actions():
                    if not thread.is_alive():
                        print('Enter is pressed')
                        break

        except KeyboardInterrupt:
            print('Ctrl+C is pressed')

        print(f'Script is terminated. {fish_count} fish caught')

    @staticmethod
    def config_parameters() -> list[ConfigParameter]:
        excluded_params = {'fishing_method', 'anti_afk'}

        enable_anti_afk_doc = 'Whether to enable anti-AFK actions. Defaults to ``True``.'
        return [
            *(
                cp
                for cp in ConfigParameter.function_params(Fisher.__init__)
                if cp.name not in excluded_params
                ),
            ConfigParameter('enable_anti_afk', bool, enable_anti_afk_doc, True),
            ]

    @staticmethod
    def from_config(config: Config, /) -> 'Fisher':
        kwargs = {
            k: v for k, v in config.params.items()
            if not isinstance(v, dict)
            }

        return Fisher(
            BaseMethod.from_config(config),
            AntiAFK.from_config(config) if kwargs.pop('enable_anti_afk', True) else None,
            **kwargs,
            )


__all__ = 'Fisher',
