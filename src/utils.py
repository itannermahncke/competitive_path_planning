from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class CellIndex:
    row: int
    col: int


@dataclass(frozen=True)
class Move:
    dy: int
    dx: int


class Action(Enum):
    UP = Move(-1, 0)
    DOWN = Move(1, 0)
    LEFT = Move(0.0, -1)
    RIGHT = Move(0, 1)


class Occupancy(Enum):
    EMPTY = 0
    OBSTACLE = -1
    PURSUANT = 1
    EVADER = 2
