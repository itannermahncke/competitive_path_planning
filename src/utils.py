from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class CellIndex:
    row: int
    col: int




class Occupancy(Enum):
    # enum - words mapped to numbers
    EMPTY = 0
    OBSTACLE = 1
    PURSUANT = 2
    EVADER = 3


class Role():
    MINIMIZER = False
    MAXIMIZER = True


@dataclass
class Node:
    depth: int
    state: str
    value: float
    role: Role
    parent: 'Node' = None
    prune: bool

    def to_dict(self):
        return {

                "depth": self.depth,
                "state": self.state,
                "value": self.value,
                "role": self.role,
        }