from threading import Thread
from time import sleep

import pyautogui as pag

from .methods.base import BaseMethod


def _ask_input():
    _ = input('Press Enter to exit\n')


def start_fishing(
        fishing_method: BaseMethod,
        /,
        fish_limit: float = 50,
        do_initial_cast: bool = True,
        ):
    """
    :param fishing_method: a method of fishing; used to cast the fishing rod and catch fish.
    :param fish_limit: the maximum number of fish to catch.
      Defaults to 50.
    :param do_initial_cast: whether to immediately cast the fishing rod when fishing loop starts.
      Defaults to ``True``.
    """
    fish_count = 0
    try:
        pag.FAILSAFE = False

        print('Switch to Destiny 2 window. Ensure it is active while script is running')

        for time in range(5, 0, -1):
            print(f'Starting in {time}s', end='\r')
            sleep(1)

        thread = Thread(target=_ask_input, daemon=True)
        thread.start()

        anti_afk = fishing_method.anti_afk
        # Loop anti-afk only if fish limit is reached
        loop_anti_afk = False

        for b in fishing_method.start(do_initial_cast):
            fish_count += b
            if fish_count >= fish_limit:
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


__all__ = 'start_fishing',
