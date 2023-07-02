from typing import NamedTuple


class Localization(NamedTuple):
    bbox_x0: int
    bbox_y0: int


del NamedTuple

russian_1920x1080 = Localization(bbox_x0=859, bbox_y0=729)
english_1920x1080 = Localization(bbox_x0=884, bbox_y0=729)
