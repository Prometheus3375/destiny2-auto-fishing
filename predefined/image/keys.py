from os import path
from typing import NamedTuple

directory = path.dirname(__file__)


class Key(NamedTuple):
    name: str
    image_path: str
    tolerance: int
    is_mouse_button: bool = False


del NamedTuple, path

E_1920x1080 = Key('e', f'{directory}\\E 1920x1080.png', tolerance=85)
