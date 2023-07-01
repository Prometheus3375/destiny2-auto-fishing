from typing import NamedTuple


class Key(NamedTuple):
    name: str
    x_averages: list[int]
    y_averages: list[int]
    tolerance: int


del NamedTuple

E_1920x1080 = Key(
    'e',
    x_averages=[97, 72, 60, 56, 54, 53, 139, 188, 151, 103, 102, 102, 102, 102, 102, 102, 100,
                84, 54, 53, 54, 58, 66, 80],
    y_averages=[79, 66, 57, 52, 147, 142, 70, 70, 69, 70, 128, 139, 69, 70, 69, 69, 70, 71,
                149, 149, 53, 60, 75, 143],
    tolerance=60,
    )
