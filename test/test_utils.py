"""
Test helper functions in utils.py.
"""

from src.environment import Environment
from src.utils import (
    CellIndex,
    Action,
    Role,
    Occupancy,
    role_to_occupancy,
    occupancy_to_role,
    derive_action,
    get_adversary,
)

import pytest

# --- test occupancy-role conversion ---


@pytest.fixture
def empty_env():
    """Create a simple 4x4 environment with no obstacles."""
    env = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(1, 1),
        evader_pos=CellIndex(1, 3),
    )
    return env


def test_pursuant_conversion():
    """
    Test that pursuants convert properly in both directions.
    """
    R_pursuant = Role.PURSUANT
    O_pursuant = Occupancy.PURSUANT
    assert O_pursuant == role_to_occupancy(R_pursuant)
    assert R_pursuant == occupancy_to_role(O_pursuant)


def test_evader_conversion():
    """
    Test that evaders convert properly in both directions.
    """
    R_evader = Role.EVADER
    O_evader = Occupancy.EVADER
    assert O_evader == role_to_occupancy(R_evader)
    assert R_evader == occupancy_to_role(O_evader)


def test_non_agent_conversion():
    """
    Test that a non-agent Occupancy converts to None.
    """
    assert occupancy_to_role(Occupancy.EMPTY) is None
    assert occupancy_to_role(Occupancy.OBSTACLE) is None


# --- test adversary finding ---


def test_pursuant_adversary():
    """
    Test that pursuant's adversary is evader
    """
    assert Role.EVADER == get_adversary(Role.PURSUANT)


def test_evader_adversary():
    """
    Test that evader's adversary is pursuant
    """
    assert Role.PURSUANT == get_adversary(Role.EVADER)


# --- test action derivation ---


def test_left_action(empty_env: Environment):
    """
    Test that when given an agent's position before and after moving left, derive_action will return the left action
    """
    a = Role.PURSUANT
    mv = Action.LEFT
    origin = empty_env.get_agent_cell(a)
    empty_env.move_agent(a, mv)
    dest = empty_env.get_agent_cell(a)
    assert mv == derive_action(origin, dest)


def test_right_action(empty_env: Environment):
    """
    Test that when given an agent's position before and after moving right, derive_action will return the right action
    """
    a = Role.PURSUANT
    mv = Action.RIGHT
    origin = empty_env.get_agent_cell(a)
    empty_env.move_agent(a, mv)
    dest = empty_env.get_agent_cell(a)
    assert mv == derive_action(origin, dest)


def test_up_action(empty_env: Environment):
    """
    Test that when given an agent's position before and after moving up, derive_action will return the up action
    """
    a = Role.PURSUANT
    mv = Action.UP
    origin = empty_env.get_agent_cell(a)
    empty_env.move_agent(a, mv)
    dest = empty_env.get_agent_cell(a)
    assert mv == derive_action(origin, dest)


def test_down_action(empty_env: Environment):
    """
    Test that when given an agent's position before and after moving down, derive_action will return the down action
    """
    a = Role.PURSUANT
    mv = Action.DOWN
    origin = empty_env.get_agent_cell(a)
    empty_env.move_agent(a, mv)
    dest = empty_env.get_agent_cell(a)
    assert mv == derive_action(origin, dest)


def test_not_action(empty_env: Environment):
    """
    Test that attempting to derive an impossible action will fail
    """
    origin = CellIndex(0, 0)
    dest = CellIndex(0, 2)
    assert derive_action(origin, dest) is None
