"""Decide actions for pursuer and evader"""

import numpy as np

from environment import Environment
from utils import Occupancy, CellIndex, Role, Node


class MiniMaxAgent:
    """
    Implementing the minimax algorithm for an agent.

    Attributes:
        agent    
    """

    def __init__(self, is_maximizer: Role, start_loc):
        """Initialize instance of MinMaxAgent class.
        
        Args:
            role: 
            is_maximizer (bool): true if agent wants to maximize
        """

        # Attributes
        self.is_maximizer = is_maximizer

        self.loc: CellIndex = start_loc
        
        self.depth = 3          # number of look-ahead moves
        self.tree_log = []      # this should be a list of lists representing each tree

        print(f"------ INITIALIZING {"EVADER" if self.is_maximizer else "PURSUANT"} ------")

    def build_tree(self, env: Environment):
        """
        Calculate all possible paths of depth
        
        Returns:
            tree:
        """
        # For each timestep agent compute
        # Implementation to create a node list of dictionaries
        # Of class Node, with set depth

        node_list = []

        # start with position
        for _ in range(self.depth):
            # A list containing the index of every empty cell
            empty_list = env.get_valid_moves()

            # Assign values to each empty position
            weight_list = self.position_eval(empty_list)

            for val in weight_list:
                # Create a node for each branching decision
                node = Node()
                # EX: node = Node(0, "S0", 2, Role.MAXIMIZER, False)

                # Appending nodes will auto populat based on depths
                node_list.append(node)

        # Log the decision tree for current compute
        self.tree_log.append(node_list)
        
    def position_eval(self, ):
            """
            Evaluates the value of Manhattan distance.   

            Args:
                empty_list: a list of the empty indices from current position
            Returns:
                weight_list: a list repopulated with the weight     
            """
            # TODO: From the given empty index and the other agents location, calculate a value to describe the distance.
            pass

    def minimax(self, nodes, depth):
        """
        Recursive function to output the min/max value.
        Prune the branch if...
        
        Args:
            nodes - possible paths for current timestep
            depth - 
        """
        val = 0


        # Exit on base case
        if depth == 0:
            return val      # Return the val which maps to a CellIndex


        if self.is_maximizer:
            max_eval = -float('inf')
            for n_sub in nodes:
                eval = self.minimax(n_sub, depth-1)       # Input args
                min_eval = max(eval, min_eval)
                # Pruning implementation
            return max_eval
        else:
            min_eval = float('inf')
            for n_sub in nodes:
                eval = self.minimax(n_sub, depth-1)       # Input args
                min_eval = min(eval, max_eval)
                # Pruning implementation
            return min_eval

    def _get_next(self, env, self_pos: CellIndex, opp_pos: CellIndex) -> CellIndex:
        """
        Calls minimax to compute next best move.
        
        Args:
            env: a game state
            self_pos: position of agent
            opp_pos: position of opponent agent
        
        Return:
            CellIndex of next location
        """
        self.build_tree(env, self_pos, opp_pos)
        best_move = self.minimax(nodes=self.tree_log[-1], depth=self.depth)

        # Internally update location
        self.loc = best_move

        return best_move
        