from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class CellIndex:
    row: int
    col: int

    # forces attributes to be simple ints, making CellIndex hashable (necessary for BFS)
    def __post_init__(self):
        # ensure values are hashable ints, not np.int64
        object.__setattr__(self, "row", int(self.row))
        object.__setattr__(self, "col", int(self.col))


@dataclass(frozen=True)
class Move:
    dy: int
    dx: int


class Action(Enum):
    UP = Move(-1, 0)
    DOWN = Move(1, 0)
    LEFT = Move(0, -1)
    RIGHT = Move(0, 1)


class Occupancy(Enum):
    EMPTY = -1
    EVADER = 0  # falsy
    PURSUANT = 1  # truthy
    OBSTACLE = 2


class Role(Enum):
    PURSUANT = False
    EVADER = True


@dataclass
class Node:
    depth: int
    id: int
    pursuant_state: CellIndex
    evader_state: CellIndex
    role: Role
    parent: int
    children: list[int]

    def to_dict(self):
        return {
            "depth": self.depth,
            "state": self.state,
            "value": self.value,
            "role": self.role,
        }
