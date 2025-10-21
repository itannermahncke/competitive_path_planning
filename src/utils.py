from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class CellIndex:
    row: int
    col: int


class Occupancy(Enum):
    EMPTY = 0
    OBSTACLE = -1
    PURSUANT = 1
    EVADER = 2
