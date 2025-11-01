from typing import List, Optional
from environment import Environment
from utils import Role, Node, get_adversary, CellIndex
import math


class MiniMax:
    """
    Minimax for the pursuer-evader game (without alpha-beta pruning).

    Usage notes:
      - Call minimax(root_node, depth, env) where `depth` is the number of plies
        (each ply is one agent move). This implementation treats `depth == 0`
        as the leaf/base case (no further lookahead).
      - root_node.agent_role should indicate which agent moves first.
      - The function returns the heuristic value (distance) for that node.
      - To choose an action, call construct_children(root, env) and pick
        the child with best minimax value.
    """

    def __init__(self):
        pass

    def minimax(
        self,
        node: Node,
        depth: int,
        env: Environment,
    ) -> Optional[float]:
        """
        Standard minimax (no alpha-beta pruning).

        Returns:
            float: heuristic value (distance) for `node` when both players play optimally.
            None: if something invalid happens (e.g., no path exists).
        """
        if node.distance is None:
            return None

        # Base case: no more lookahead OR capture adjacency reached
        if depth == 0 or node.distance == 1:
            return node.distance

        # Generate possible moves
        children = self.construct_children(node, env)
        if not children:
            return node.distance

        # EVADER maximizes distance
        if node.agent_role == Role.EVADER:
            max_eval = -math.inf
            for child in children:
                val = self.minimax(child, depth - 1, env)
                if val is None:
                    continue
                max_eval = max(max_eval, val)
            return max_eval

        # PURSUANT minimizes distance
        else:
            min_eval = math.inf
            for child in children:
                val = self.minimax(child, depth - 1, env)
                if val is None:
                    continue
                min_eval = min(min_eval, val)
            return min_eval

    def evaluate_heuristic(self, node: Node, env: Environment) -> Optional[int]:
        """
        Evaluate heuristic for a node: shortest path distance
        between pursuant_state and evader_state.
        """
        return env.get_shortest_distance(node.pursuant_state, node.evader_state)

    def construct_children(self, node: Node, env: Environment) -> List[Node]:
        """
        Build child Node objects for `node`, for every legal move of node.agent_role.

        Does not mutate the environment; uses node’s stored positions.
        """
        children: List[Node] = []

        agent_to_move = node.agent_role
        cur_pos = (
            node.pursuant_state if agent_to_move == Role.PURSUANT else node.evader_state
        )

        # valid destinations around cur_pos (ignores obstacles)
        neighbors = env.get_neighbors(cur_pos)

        for dest in neighbors:
            if agent_to_move == Role.PURSUANT:
                new_p = dest
                new_e = node.evader_state
            else:
                new_p = node.pursuant_state
                new_e = dest

            dist = env.get_shortest_distance(new_p, new_e)

            child_node = Node(
                depth=max(0, node.depth - 1) if hasattr(node, "depth") else 0,
                agent_role=get_adversary(agent_to_move),
                pursuant_state=new_p,
                evader_state=new_e,
                distance=dist,
                children_list=[],
            )
            children.append(child_node)

        node.children_list = children
        return children

    def choose_action(self, root: Node, lookahead_depth: int, env: Environment):
        """
        Return the best child Node (action) and its minimax value.
        """
        children = self.construct_children(root, env)
        if not children:
            return None, None

        best_child = None
        if root.agent_role == Role.EVADER:
            best_value = -math.inf
            for child in children:
                val = self.minimax(child, lookahead_depth - 1, env)
                if val is not None and val > best_value:
                    best_value = val
                    best_child = child
        else:  # PURSUANT minimizes
            best_value = math.inf
            for child in children:
                val = self.minimax(child, lookahead_depth - 1, env)
                if val is not None and val < best_value:
                    best_value = val
                    best_child = child

        return best_child, best_value
