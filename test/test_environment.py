import pytest
import math
from src.environment import Environment
from src.utils import Occupancy, CellIndex, Action

# --- Fixtures ---

# Fixtures are used to provide standard setup for unit tests. They can be passed to other unit tests as parameters, giving them access to standard variables.


@pytest.fixture
def empty_env():
    """Create a simple 4x4 environment with no obstacles."""
    env = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=CellIndex(3, 3),
    )
    return env


@pytest.fixture
def sparse_env():
    """Create a simple 4x4 environment with two obstacles."""
    env = Environment(
        size=4,
        density=0.0,
        pursuant_pos=CellIndex(0, 0),
        evader_pos=CellIndex(3, 3),
    )
    env.place_additional_obstacles([CellIndex(1, 0), CellIndex(1, 1)])
    return env


@pytest.fixture
def dense_env():
    """Create a simple 4x4 environment with many obstacles."""
    env = Environment(
        size=4,
        density=0.5,
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
        evader_pos=CellIndex(0, 1),
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
        evader_pos=CellIndex(0, 1),
    )
    assert len(env.get_obstacle_cells()) == math.floor(env.size**2 * d)


# --- Unit tests for _get() and _set() ---


def test_set_and_get_valid_cell(empty_env: Environment):
    """
    Test that _set() and _get() correctly update and read a cell.
    """
    cell = CellIndex(2, 2)
    empty_env._set(cell, Occupancy.OBSTACLE)
    assert empty_env._get(cell) == Occupancy.OBSTACLE


def test_set_invalid_cell(empty_env: Environment):
    """
    Test that _set() does not change the environment when the cell is invalid.
    """
    invalid = CellIndex(-1, 0)
    current_value = empty_env._get(invalid)
    empty_env._set(invalid, Occupancy.OBSTACLE)
    assert current_value == empty_env._get(invalid)


def test_get_invalid_cell(empty_env: Environment):
    """
    Test that _get() returns None when the cell is invalid.
    """
    invalid = CellIndex(-1, 0)
    val = empty_env._get(invalid)
    assert val is None


# --- Unit tests for editing cells ---


def test_place_invalid_obstacles(empty_env: Environment):
    """
    Test that the environment will not replace agents with obstacles.
    """
    pursuant = CellIndex(0, 0)
    evader = CellIndex(3, 3)
    obs = [pursuant, evader]
    placed = empty_env.place_additional_obstacles(obs)
    assert len(placed) == 0
    assert empty_env._get(pursuant) == Occupancy.PURSUANT
    assert empty_env._get(evader) == Occupancy.EVADER


def test_place_out_of_bounds_obstacles(empty_env: Environment):
    """
    Test that the environment will not place obstacles out-of-bounds.
    """
    o = CellIndex(-1, 0)
    obs = [o]
    placed = empty_env.place_additional_obstacles(obs)
    assert len(placed) == 0


def test_valid_obstacles(empty_env: Environment):
    """
    Test that the environment can place multiple obstacles in valid positions.
    """
    o1 = CellIndex(1, 1)
    o2 = CellIndex(2, 2)
    obs = [o1, o2]
    placed = empty_env.place_additional_obstacles(obs)
    assert len(placed) == 2
    assert empty_env._get(o1) == Occupancy.OBSTACLE
    assert empty_env._get(o2) == Occupancy.OBSTACLE


def test_move_agent_success(sparse_env: Environment):
    """
    Test that move_agent() successfully moves an agent to an empty cell.
    """
    origin = sparse_env.get_agent_cell(Occupancy.PURSUANT)
    dest = CellIndex(origin.row, origin.col + 1)
    success = sparse_env.move_agent(Occupancy.PURSUANT, Action.RIGHT)
    assert success
    assert sparse_env._get(origin) == Occupancy.EMPTY
    assert sparse_env.get_agent_cell(Occupancy.PURSUANT) == dest


def test_move_correct_agent(sparse_env: Environment):
    """
    Test that move_agent() does not adjust the position of the other agent.
    """
    alt_origin = CellIndex(3, 3)
    success = sparse_env.move_agent(Occupancy.PURSUANT, Action.RIGHT)
    assert success
    assert sparse_env._get(alt_origin) == Occupancy.EVADER


def test_move_agent_illegal_occupied(sparse_env: Environment):
    """
    Test that move_agent() fails when target cell is not empty.
    """
    origin = CellIndex(0, 0)
    success = sparse_env.move_agent(Occupancy.PURSUANT, Action.DOWN)
    assert not success
    assert sparse_env.get_agent_cell(Occupancy.PURSUANT) == origin


def test_move_agent_illegal_bounds(sparse_env: Environment):
    """
    Test that move_agent() fails when target cell is out of bounds.
    """
    origin = CellIndex(0, 0)
    success = sparse_env.move_agent(Occupancy.PURSUANT, Action.LEFT)
    assert not success
    assert sparse_env.get_agent_cell(Occupancy.PURSUANT) == origin


# --- Unit tests for locating cells ---
# get_agent_cell(), get_obstacle_cells()


def test_get_agent_cell(empty_env: Environment):
    """
    Test that get_agent_cell() returns the correct location for each agent.
    """
    assert empty_env.get_agent_cell(Occupancy.PURSUANT) == CellIndex(0, 0)
    assert empty_env.get_agent_cell(Occupancy.EVADER) == CellIndex(3, 3)


def test_get_obstacle_cells_none(empty_env: Environment):
    """
    Test that get_obstacle_cells() returns no obstacles for an empty environment.
    """
    result = empty_env.get_obstacle_cells()
    assert len(result) == 0
    assert result == []


def test_get_obstacle_cells_some(sparse_env: Environment):
    """
    Test that get_obstacle_cells() returns the correct location for each obstacle.
    """
    result = sparse_env.get_obstacle_cells()
    assert len(result) == 2
    for obs in result:
        assert obs in [CellIndex(1, 0), CellIndex(1, 1)]


# --- Unit tests for analyzing cells ---
# get_neighbors(), get_valid_moves(), get_shortest_distance()


# def test_get_neighbors(simple_env):
#     """Test that get_neighbors() returns all valid non-obstacle adjacent cells."""
#     pass


# def test_get_neighbors_with_obstacles(simple_env):
#     """Test that get_neighbors() excludes obstacle cells."""
#     pass


# def test_get_shortest_distance_straight_path(simple_env):
#     """Test BFS distance in an empty grid (no obstacles)."""
#     pass


# def test_get_shortest_distance_blocked(simple_env):
#     """Test BFS returns None when no path exists due to obstacles."""
#     pass


# --- Unit tests for analyzing game state ---
# is_within_bounds(), is_pursuant_win()


def test_within_bounds(empty_env: Environment):
    """Test that is_within_bounds() correctly identifies valid cells."""
    assert empty_env.is_within_bounds(CellIndex(0, 0))


def test_out_of_bounds(empty_env: Environment):
    """
    Test that is_within_bounds() correctly identifies invalid cells.
    """
    assert not empty_env.is_within_bounds(CellIndex(-1, 0))


def test_pursuant_win_vertical():
    """
    Test that is_pursuant_win() detects adjacency in the vertical direction.
    """
    env1 = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(2, 3),
        evader_pos=CellIndex(3, 3),
    )
    assert env1.is_pursuant_win()

    env2 = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(3, 3),
        evader_pos=CellIndex(2, 3),
    )
    assert env2.is_pursuant_win()


def test_pursuant_win_horizontal():
    """
    Test that is_pursuant_win() detects adjacency in the horizontal direction.
    """
    env1 = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(3, 2),
        evader_pos=CellIndex(3, 3),
    )
    assert env1.is_pursuant_win()

    env2 = Environment(
        size=5,
        density=0.0,
        pursuant_pos=CellIndex(3, 3),
        evader_pos=CellIndex(3, 2),
    )
    assert env2.is_pursuant_win()


def test_not_pursuant_win(empty_env: Environment):
    """
    Test that is_pursuant_win() detects adjacency correctly.
    """
    assert not empty_env.is_pursuant_win()
