import pytest
import math
from src.environment import Environment
from src.utils import Occupancy, CellIndex, Action

# --- Fixtures ---

# Fixtures are used to provide standard setup for unit tests. They can be passed to other unit tests as parameters, giving them access to standard variables.


@pytest.fixture
def empty_tree(depth=3):
    """Create an empty tree of depth 3 with populated values."""
    pass

####################################
    # UNIT TESTS FOR INIT #
####################################




####################################
  # UNIT TESTS FOR BUILDING TREE #
####################################

def test_tree_depth():
    """
    Test that the decision tree has x levels of depth
    """
    pass

####################################
# UNIT TESTS FOR MINIMAX ALGORITHM #
####################################

def test_maximizer_eval():
    """
    Test the output val of maximizer turn.
    """
    pass


def test_minimizer_eval():
    """
    Test the output val of minimizer turn.
    """
    pass


def test_maximizer_pruning():
    """
    Test pruning branches for maximizer.
    """
    pass

def test_minimizer_pruning():
    """
    Test pruning branches for minimizer.
    """
    pass