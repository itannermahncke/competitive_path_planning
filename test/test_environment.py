import pytest
import math
from environment import Environment
from utils import Occupancy, CellIndex

# --- Fixtures ---

# Fixtures are used to provide standard setup for unit tests. They can be passed to other unit tests as parameters, giving them access to standard variables.


@pytest.fixture
def empty_env():
    """Create a simple 6x6 environment with no obstacles."""
    env = Environment(
        size=5,
        density=0.25,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=CellIndex(3, 3),
    )
    return env


@pytest.fixture
def sparse_env():
    """Create a simple 6x6 environment with sparse obstacles."""
    env = Environment(
        size=5,
        density=0.16,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=CellIndex(3, 3),
    )
    return env


@pytest.fixture
def dense_env():
    """Create a simple 6x6 environment with many obstacles."""
    env = Environment(
        size=5,
        density=0.33,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=CellIndex(3, 3),
    )
    return env


# --- Unit tests For __init__() ---


def test_correct_dimensions():
    """
    Test that the environment's dimensions match the desired size.
    """
    env = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=(0, 1),
    )
    assert env.size == 5
    assert env.is_within_bounds(CellIndex(4, 4))


def test_correct_agent_placement():
    """
    Test that both agents are properly placed in the environment.
    """
    pursuant = CellIndex(0, 0)
    evader = CellIndex(0, 1)
    env = Environment(
        size=5,
        density=0.0,
        pursuant_pos=pursuant,
        evader_pos=evader,
    )
    assert env.get_agent_cell(Occupancy.PURSUANT) == pursuant
    assert env.get_agent_cell(Occupancy.EVADER) == evader


def test_correct_obstacle_density():
    """
    Test that the environment generated the proper number of obstacles.
    """
    d = 0.2
    env = Environment(
        size=5,
        density=d,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=(0, 1),
    )
    assert len(env.get_obstacle_cells()) == math.floor(env.size**2 * d)


# --- Unit tests for _get() and _set() ---


def test_set_and_get_valid_cell(empty_env):
    """
    Test that _set() and _get() correctly update and read a cell.
    """
    cell = CellIndex(2, 2)
    empty_env._set(cell, Occupancy.OBSTACLE)
    assert empty_env._get(cell) == Occupancy.OBSTACLE


def test_set_invalid_cell(empty_env):
    """
    Test that _set() does not change the environment when the cell is invalid.
    """
    invalid = CellIndex(-1, 0)
    current_value = empty_env._get(invalid)
    empty_env._set(invalid, Occupancy.OBSTACLE)
    assert current_value == empty_env._get(invalid)


def test_get_invalid_cell(simple_env):
    """
    Test that _get() returns None when the cell is invalid.
    """
    invalid = CellIndex(-1, 0)
    val = simple_env._get(invalid)
    assert val is None


# --- Unit tests for editing cells ---
# move_agent()


def test_move_agent_success(empty_env):
    """
    Test that move_agent() successfully moves an agent to an empty cell.
    """
    pass


def test_move_agent_illegal_occupied(empty_env):
    """
    Test that move_agent() fails when target cell is not empty.
    """
    pass


def test_move_agent_illegal_bounds(empty_env):
    """
    Test that move_agent() fails when target cell is out of bounds.
    """
    pass


# --- Unit tests for locating cells ---
# get_agent_cell(), get_obstacle_cells()


def test_get_agent_cell(simple_env):
    """Test that get_agent_cell() returns the correct location for each agent."""
    pass


def test_get_obstacle_cells_none(simple_env):
    """Test that get_agent_cell() returns the correct location for each agent."""
    pass


def test_get_obstacle_cells_some(simple_env):
    """Test that get_agent_cell() returns the correct location for each agent."""
    pass


# --- Unit tests for analyzing cells ---
# get_neighbors(), get_valid_moves(), get_shortest_distance()


def test_get_neighbors(simple_env):
    """Test that get_neighbors() returns all valid non-obstacle adjacent cells."""
    pass


def test_get_neighbors_with_obstacles(simple_env):
    """Test that get_neighbors() excludes obstacle cells."""
    pass


def test_get_shortest_distance_straight_path(simple_env):
    """Test BFS distance in an empty grid (no obstacles)."""
    pass


def test_get_shortest_distance_blocked(simple_env):
    """Test BFS returns None when no path exists due to obstacles."""
    pass


# --- Unit tests for analyzing game state ---
# is_within_bounds(), is_pursuant_win()


def test_within_bounds(simple_env):
    """Test that is_within_bounds() correctly identifies valid/invalid cells."""
    pass


def test_ut_of_bounds(simple_env):
    """Test that is_within_bounds() correctly identifies valid/invalid cells."""
    pass


def test_pursuant_win(simple_env):
    """Test that is_pursuant_win() detects adjacency correctly."""
    pass


def test_not_pursuant_win(simple_env):
    """Test that is_pursuant_win() detects adjacency correctly."""
    pass
