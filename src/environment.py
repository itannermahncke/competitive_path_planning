""" """

from collections import deque
import numpy as np
import random
import math

from src.utils import Occupancy, Role, CellIndex, Action, role_to_occupancy


class Environment:
    """
    The Environment class models the occupancy grid playing field that the two agents traverse as they compete.

    Attributes:
        _graph (nparray): The occupancy grid where the game state is stored.
        _size (int): The dimensions of the square environment.
    """

    def __init__(
        self,
        size: int,
        density: float,
        pursuant_pos: CellIndex,
        evader_pos: CellIndex,
    ):
        """
        Initialize a new instance of the Environment class with obstacle density.

        Args:
            size (int): The dimensions of the square environment
            density (float): The percentage of cells in the environment to populate with obstacles
            pursuant_pos (CellIndex): Starting position of the pursuant agent.
            evader_pos (CellIndex): Starting position of the evader agent.
            pursuant (Occupany): A pursuant agent
            evader (Occupany): An evader agent

        """
        # create attributes
        self._graph = np.full((size, size), Occupancy.EMPTY, dtype=Occupancy)
        self._size = size

        # place agents
        self._set(pursuant_pos, Occupancy.PURSUANT)
        self._set(evader_pos, Occupancy.EVADER)

        # place obstacles based on density
        for _ in range(0, math.floor(size**2 * density)):
            while True:
                row = random.randint(0, size - 1)
                col = random.randint(0, size - 1)
                # Check if CellIndex is empty (including agent occupancy)
                if self._graph[row][col] == Occupancy.EMPTY:
                    self._graph[row][col] = Occupancy.OBSTACLE
                    break

    @property
    def size(self):
        return self._size

    def place_additional_obstacles(self, obstacles: list[CellIndex]) -> list[CellIndex]:
        """
        Add additional obstacles to the world from a list. If their indexes do not fall within bounds or fall on an occupied cell, they will be skipped.

        Args:
            obstacles (list[CellIndex]): the obstacles to place

        Returns:
            A list of the obstacles that were actually placed in the world.
        """
        placed_obstacles = []
        # place obstacles based on list
        for obs in obstacles:
            if self.is_within_bounds(obs) and self._get(obs) == Occupancy.EMPTY:
                self._set(obs, Occupancy.OBSTACLE)
                placed_obstacles.append(obs)
        return placed_obstacles

    def move_agent(self, agent: Role, action: Action) -> bool:
        """
        Move an agent from one place to another.

        Args:
            agent (Role): agent to move
            action (Action): action to enact

        Returns:
            The success of the operation.
        """
        # fail if dest is not empty
        cur_pos = self.get_agent_cell(agent)
        new_pos = CellIndex(
            cur_pos.row + action.value.dy, cur_pos.col + action.value.dx
        )
        if self._get(new_pos) != Occupancy.EMPTY:
            print("Illegal move action!")
            return False

        # move the agent
        self._set(cur_pos, Occupancy.EMPTY)
        self._set(new_pos, role_to_occupancy(agent))
        return True

    def get_agent_cell(self, agent: Role) -> CellIndex:
        """
        Find and return an agent's location in the environment.

        Args:
            agent (Role): The agent to locate.

        Returns:
            The index of the cell where the agent is located.
        """
        agent = role_to_occupancy(agent)
        for i, r in enumerate(self._graph):
            if agent in r:
                return CellIndex(i, np.where(r == agent)[0])
        print("Agent could not be found")
        return None

    def get_obstacle_cells(self) -> list[CellIndex]:
        """
        Provide a list of cell indexes containing obstacles.

        Returns:
            A list of all obstacle-occupied cells in the environment.
        """
        obstacles = []
        for i in range(0, self._size):
            for j in range(0, self._size):
                if self._get(CellIndex(i, j)) == Occupancy.OBSTACLE:
                    obstacles.append(CellIndex(i, j))
        return obstacles

    def get_neighbors(self, cell: CellIndex) -> list[CellIndex]:
        """
        Provide a list of empty cells around the given cell.

        Args:
            cell (CellIndex): Index of cell to find neighbors of.

        Returns:
            A list containing the index of every empty cell adjacent to cell.
        """
        neighbors = []
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for offset in offsets:
            neighbor = CellIndex(cell.row + offset[0], cell.col + offset[1])
            if self.is_within_bounds(neighbor):
                if self._get(neighbor) == Occupancy.EMPTY:
                    neighbors.append(neighbor)
        return neighbors

    def get_valid_moves(self, agent: Role) -> list[CellIndex]:
        """
        Provide a list of empty cells around a given agent.

        Args:
            agent (Role): Agent to find the neighbors of.

        Returns:
            A list containing the index of every empty cell adjacent to the agent.
        """
        # setup and find agent
        agent_cell = self.get_agent_cell(agent)
        if agent_cell is None:
            return

        return self.get_neighbors(agent_cell)

    def get_shortest_distance(self, cell1: CellIndex, cell2: CellIndex):
        """
        Return the number of steps between the given cells, accounting for obstacles. Found using breadth-first search.

        Args:
            cell1: Starting point of BFS distance
            cell2: Ending point of BFS distance
        """
        # verification
        if not self.is_within_bounds(cell1) or not self.is_within_bounds(cell2):
            print("cells are not valid!")
            return None

        # breadth-first search
        visited = set([cell1])
        queue = deque([(cell1, 0)])  # store (node, distance)

        while queue:
            current, dist = queue.popleft()
            if current == cell2:
                return dist  # number of edges in shortest path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        # no path found
        return None

    def is_within_bounds(self, cell: CellIndex):
        """
        Check if the given cell index is within the bounds of the environment.

        Args:
            cell (CellIndex): The cell to evaluate.

        Returns:
            Whether or not the cell is within the grid.
        """
        return 0 <= cell.row < self._size and 0 <= cell.col < self._size

    def is_pursuant_win(self):
        """
        Check and return if the pursuant is adjacent to the evader.

        Returns:
            True if so, False otherwise.
        """
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        pursuant_cell = self.get_agent_cell(Role.PURSUANT)
        if pursuant_cell is None:
            return
        for offset in offsets:
            neighbor = CellIndex(
                pursuant_cell.row + offset[0], pursuant_cell.col + offset[1]
            )
            if self.is_within_bounds(neighbor):
                if self._get(neighbor) == Occupancy.EVADER:
                    return True
        return False

    def _set(self, cell: CellIndex, value: Occupancy):
        """
        Set the occupancy of a cell in graph at a particular index.
        """
        # private, only called by environment
        if not self.is_within_bounds(cell):
            print("Not a valid cell!")
            return
        self._graph[cell.row][cell.col] = value

    def _get(self, cell: CellIndex) -> Occupancy:
        """
        Get value of cell in graph at a particular index.
        """
        if not self.is_within_bounds(cell):
            print("Not a valid cell!")
            return None
        return self._graph[cell.row][cell.col]
