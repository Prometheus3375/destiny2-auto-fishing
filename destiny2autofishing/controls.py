from time import sleep

# noinspection PyProtectedMember
from pyautogui._pyautogui_win import _click, _keyDown, _keyUp, _mouseDown, _mouseUp, _position

KEY_PRESS_DURATION = 0.2
"""
Sleep time between down and up operations inside function ``press_key``.
"""


def press_key(key: str, /):
    _keyDown(key)
    # Sometimes Destiny 2 fails to capture key presses
    # if there is no sleep or sleep time is low.
    # Value of 0.1 sometimes fails (usually at low FPS), so I put 0.2.
    sleep(KEY_PRESS_DURATION)
    _keyUp(key)


def hold_key(key: str, hold_duration: float, /):
    _keyDown(key)
    sleep(hold_duration)
    _keyUp(key)


def press_mouse(button: str, /):
    x, y = _position()
    _click(x, y, button)


def hold_mouse(button: str, hold_duration: float, /):
    x, y = _position()
    _mouseDown(x, y, button)
    sleep(hold_duration)
    x, y = _position()
    _mouseUp(x, y, button)


__all__ = 'press_key', 'press_mouse', 'hold_key', 'hold_mouse'
