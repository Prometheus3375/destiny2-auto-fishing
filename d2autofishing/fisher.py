from threading import Thread
from time import sleep

import pyautogui as pag

from .methods.base import BaseMethod


def _ask_input():
    _ = input('Press Enter to exit\n')


def start_fishing(
        fishing_method: BaseMethod,
        /,
        fish_limit: int,
        do_initial_cast: bool,
        ):
    """
    :param fishing_method: a method of fishing; used to cast fishing rod and catch fish.
    :param fish_limit: the maximum number of fish to catch. When reached, this function exits.
    :param do_initial_cast: whether to immediately cast fishing rod when this script starts.
    """
    fish_count = 0
    try:
        pag.FAILSAFE = False

        print('Switch to Destiny 2 window. Ensure it is active while script is running')

        # Put carriage return in the start to support PyCharm Run window output
        for time in range(5, 0, -1):
            print(f'\rStarting in {time}s', end='')
            sleep(1)
        print('\r', end='')

        thread = Thread(target=_ask_input, daemon=True)
        thread.start()

        for b in fishing_method.start(do_initial_cast):
            fish_count += b
            if fish_count >= fish_limit:
                print('Fish limit is reached; collect it and restart the script')
                break
            elif not thread.is_alive():
                print('Enter is pressed')
                break
    except KeyboardInterrupt:
        print('Ctrl+C is pressed')

    print(f'Script is terminated. {fish_count} fish caught')


__all__ = 'start_fishing',
