from enum import Enum
from dataclasses import dataclass
from typing import Optional


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


def derive_action(origin: CellIndex, dest: CellIndex):
    """
    Given a starting and ending cell, determine which action caused the operation.
    """
    operation = Move(
        dy=dest.row - origin.row,
        dx=dest.col - origin.col,
    )

    for a in Action:
        if operation == a.value:
            return a
    return None


class Occupancy(Enum):
    EMPTY = 0
    EVADER = 2
    PURSUANT = 3
    OBSTACLE = 1


class Role(Enum):
    PURSUANT = False
    EVADER = True


def get_adversary(agent: Role) -> Role:
    """
    Given an agent, return its opponent.
    """
    if agent == Role.PURSUANT:
        return Role.EVADER
    elif agent == Role.EVADER:
        return Role.PURSUANT


def occupancy_to_role(agent: Occupancy) -> Role:
    """
    Convert Occupancy representing an agent into a Role.
    """
    if agent == Occupancy.PURSUANT:
        return Role.PURSUANT
    elif agent == Occupancy.EVADER:
        return Role.EVADER
    return None


def role_to_occupancy(agent: Role) -> Occupancy:
    """
    Convert Role to Occupancy representing an agent.
    """
    if agent == Role.PURSUANT:
        return Occupancy.PURSUANT
    elif agent == Role.EVADER:
        return Occupancy.EVADER


@dataclass
class Node:
    # personal attributes
    # id: int
    depth: int
    # game state attributes
    agent_role: Role
    pursuant_state: CellIndex
    evader_state: CellIndex
    distance: int
    children_list: list
    # action_from_parent: Action
    # # relational attributes
    # parent: Optional["Node"]
    # children: list[Optional["Node"]]

    def to_dict(self):
        return {
            # "id": self.id,
            "depth": self.depth,
            "role": self.agent_role.name,
            "pursuant state": self.pursuant_state,
            "evader state": self.evader_state,
            "distance": self.distance,
            # "action taken": self.action_from_parent,
            "children list": self.children_list
        }
