""" """

from collections import deque
import numpy as np
import random
import math

from utils import Occupancy, CellIndex


class Environment:
    """
    The Environment class models the occupancy grid playing field that the two agents traverse as they compete.

    Attributes:
        _graph (nparray): The occupancy grid where the game state is stored.
        _size (int): The dimensions of the square environment.
    """

    def __init__(
        this,
        size: int,
        density: float,
        pursuant_pos: CellIndex,
        evader_pos: CellIndex,
    ):
        """
        Initialize a new instance of the Environment class.

        Args:
            size (int): The dimensions of the square environment
            density (float): The percentage of cells in the environment to populate with obstacles
        pursuant_pos (CellIndex): Starting position of the pursuant agent.
        evader_pos (CellIndex): Starting position of the evader agent.
        """
        # create attributes
        this._graph = np.full((size, size), Occupancy.EMPTY, dtype=int)
        this._size = size

        # place agents
        this._set(pursuant_pos, Occupancy.PURSUANT)
        this._set(evader_pos, Occupancy.EVADER)

        # place obstacles based on density
        for _ in range(0, math.floor(size**2 * density)):
            while True:
                row = random.randint(0, size - 1)
                col = random.randint(0, size - 1)
                if this._graph[row][col] == Occupancy.EMPTY:
                    this._graph[row][col] = Occupancy.OBSTACLE
                    break

    def move_agent(this, current_pos: CellIndex, new_pos: CellIndex) -> bool:
        """
        Move an agent from one place to another. No need to specify agent.

        Args:
            current_pos (CellIndex): Current agent location.
            new_pos (CellIndex): Desired agent location.

        Returns:
            The success of the operation.
        """
        agent = this._get(current_pos)
        # fail if no agent is there
        if agent != Occupancy.PURSUANT and agent != Occupancy.EVADER:
            print("No agent found here!")
            return False
        # fail if dest is not empty
        if this._get(new_pos) != Occupancy.EMPTY:
            print("Illegal move action!")
            return False

        # move the agent
        this._set(current_pos, Occupancy.EMPTY)
        this._set(new_pos, agent)
        return True

    def get_agent_cell(this, agent: Occupancy) -> CellIndex:
        """
        Find and return an agent's location in the environment.

        Args:
            agent (Occupancy): The enumerated agent to locate.

        Returns:
            The index of the cell where the agent is located.
        """
        if agent != Occupancy.PURSUANT and agent != Occupancy.EVADER:
            print("Not a valid agent")
            return None
        for i, r in enumerate(this._graph):
            if agent in r:
                return CellIndex(i, np.where(r == agent)[0])
        print("Agent could not be found")
        return None

    def get_neighbors(this, cell: CellIndex) -> list[CellIndex]:
        """
        Provide a list of non-obstacle cells around the given cell. This could include a neighbor containing an agent.

        Args:
            cell (CellIndex): Index of cell to find neighbors of.

        Returns:
            A list containing the index of every non-obstacle cell adjacent to this one.
        """
        neighbors = []
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for offset in offsets:
            neighbor = CellIndex(cell.row + offset[0], cell.col + offset[1])
            if this.is_within_bounds(neighbor):
                if this._get(neighbor) != Occupancy.OBSTACLE:
                    neighbors.append(neighbor)
        return neighbors

    def get_valid_moves(this, agent: Occupancy) -> list[CellIndex]:
        """
        Provide a list of empty cells around a given agent.

        Args:
            agent (Occupancy): Agent to find the neighbors of.

        Returns:
            A list containing the index of every empty cell adjacent to the agent.
        """
        # setup and find agent
        agent_cell = this.get_agent_cell(agent)
        if agent_cell is None:
            return

        neighbors = this.get_neighbors(agent_cell)
        empty_spaces = [n for n in neighbors if this._get(n) == Occupancy.EMPTY]
        return empty_spaces

    def get_shortest_distance(this, cell1: CellIndex, cell2: CellIndex):
        """
        Return the number of steps between the given cells, accounting for obstacles. Found using breadth-first search.

        Args:
            cell1: Starting point of Manhattan distance
            cell2: Ending point of Manhattan distance
        """
        # verification
        if not this.is_within_bounds(cell1) or not this.is_within_bounds(cell2):
            print("cells are not valid!")
            return None

        # breadth-first search
        visited = set([cell1])
        queue = deque([(cell1, 0)])  # store (node, distance)

        while queue:
            current, dist = queue.popleft()
            if current == cell2:
                return dist  # number of edges in shortest path

            for neighbor in this.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        # no path found
        return None

    def is_within_bounds(this, cell: CellIndex):
        """
        Check if the given cell index is within the bounds of the environment.

        Args:
            cell (CellIndex): The cell to evaluate.

        Returns:
            Whether or not the cell is within the grid.
        """
        return 0 <= cell.row < this._size and 0 <= cell.col < this._size

    def is_pursuant_win(this):
        """
        Check and return if the pursuant is adjacent to the evader.

        Returns:
            True if so, False otherwise.
        """
        pursuant_cell = this.get_agent_cell(Occupancy.PURSUANT)
        if pursuant_cell is None:
            return
        for cell in this.get_neighbors(pursuant_cell):
            if this._get(cell) == Occupancy.EVADER:
                return True

        return False

    def _set(this, cell: CellIndex, value: Occupancy):
        """
        Set the occupancy of a cell in graph at a particular index.
        """
        if not this.is_within_bounds(cell):
            print("Not a valid cell!")
            return
        this._graph[cell.row][cell.col] = value

    def _get(this, cell: CellIndex) -> Occupancy:
        """
        Get value of cell in graph at a particular index.
        """
        if not this.is_within_bounds(cell):
            print("Not a valid cell!")
            return None
        return this._graph[cell.row][cell.col]
