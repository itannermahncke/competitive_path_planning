"""
Decide actions for pursuer and evader.
"""

from utils import Role, Node


class MiniMax:
    """
    Implements the minimax algorithm with alpha-beta pruning to direct two adversarial agents.
    """

    def __init__(self):
        """
        Initialize instance of MiniMaxAgent class.
        """

    def minimax(
        self,
        node: Node,
        depth: int,
        alpha=-float("inf"),
        beta=float("inf"),
    ):
        """
        Recursive function to output the min/max value.
        Prune the branch if alpha >= beta (or min/max values are equal), since no better option will be available through this route.

        Args:
            node: a single node in the game tree representing a game state
            depth: current level in the tree, beginning with look-ahead depth
            alpha: "worst-case scenario" value for maximizer, continually increases
            beta: "worst-case scenario" value for minimizer, continually decreases
        """
        # Exit on base case: return heuristic value of node
        if depth == 0:
            return node.distance

        # Evader
        if node.agent_role == Role.EVADER:
            max_eval = -float("inf")
            for child in node.children:
                max_eval = max(
                    max_eval,
                    self.minimax(
                        child,
                        depth - 1,
                        alpha,
                        beta,
                    ),
                )
                # Pruning implementation
                if max_eval >= beta:
                    break
                alpha = max(alpha, max_eval)
            return max_eval

        # Pursuant
        else:
            min_eval = float("inf")
            for child in node.children:
                min_eval = min(
                    min_eval,
                    self.minimax(
                        child,
                        depth - 1,
                        alpha,
                        beta,
                    ),
                )
                # Pruning implementation
                if min_eval <= alpha:
                    break
                beta = min(beta, min_eval)
            return min_eval
