from typing import NamedTuple


class Localization(NamedTuple):
    bbox_x0: int
    bbox_y0: int


del NamedTuple

russian_1920x1080 = Localization(bbox_x0=857, bbox_y0=727)
english_1920x1080 = Localization(bbox_x0=882, bbox_y0=727)
