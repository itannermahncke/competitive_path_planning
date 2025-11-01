# minimax.py  (replace the contents of your current MiniMax class file)
from typing import List, Optional
from environment import Environment
from utils import Role, Node, get_adversary, CellIndex

import math

class MiniMax:
    """
    Minimax with alpha-beta pruning for the pursuer-evader game.

    Usage notes:
      - Call minimax(root_node, depth, env) where `depth` is the number of plies
        (each ply is one agent move). This implementation treats `depth == 0`
        as the leaf/base case (no further lookahead).
      - root_node.agent_role should indicate which agent is to move at the root.
      - The function returns the heuristic value (distance) for the node.
      - To choose an action for the current player you'd call construct_children(root, env)
        and pick the child with best minimax value (ties handled as you like).
    """

    def __init__(self):
        pass

    def minimax(
        self,
        node: Node,
        depth: int,
        env: Environment,
        alpha: float = -math.inf,
        beta: float = math.inf,
    ) -> Optional[float]:
        """
        Minimax with alpha-beta pruning.

        Returns:
            float: heuristic value (distance) for `node` when both players play
                   optimally to the given `depth`.
            None: if something invalid happens (e.g., no path exists and distance is None).
        """
        # Evaluate node distance (heuristic stored on node). If distance is None,
        # that means no path exists; we treat that as a large distance for evader (maximize)
        # and a large penalty for pursuant (minimize) — but here we'll return None to
        # signal invalidity unless you prefer numeric handling.
        if node.distance is None:
            return None

        # Base case: no more lookahead OR capture adjacency reached
        # (distance == 1 means pursuant adjacent to evader per your rule)
        if depth == 0 or node.distance == 1:
            return node.distance

        # Generate children for the current node (list of Node)
        children = self.construct_children(node, env)
        # If there are no legal moves for the agent to move, return current node's heuristic
        if not children:
            return node.distance

        # EVADER maximizes distance
        if node.agent_role == Role.EVADER:
            max_eval = -math.inf
            for child in children:
                val = self.minimax(child, depth - 1, env, alpha, beta)
                if val is None:
                    # propagate invalid path info (or you can map to large value)
                    return None
                if val > max_eval:
                    max_eval = val
                # update alpha
                alpha = max(alpha, max_eval)
                # pruning
                if alpha >= beta:
                    # branch pruned
                    # print("Alpha-Beta: EVADER branch pruned")
                    break
            return max_eval

        # PURSUANT minimizes distance
        else:
            min_eval = math.inf
            for child in children:
                val = self.minimax(child, depth - 1, env, alpha, beta)
                if val is None:
                    return None
                if val < min_eval:
                    min_eval = val
                # update beta
                beta = min(beta, min_eval)
                # pruning
                if beta <= alpha:
                    # print("Alpha-Beta: PURSUANT branch pruned")
                    break
            return min_eval

    def evaluate_heuristic(self, node: Node, env: Environment) -> Optional[int]:
        """
        Evaluate heuristic for a node. For now we use shortest path distance
        between pursuant_state and evader_state computed by env.
        """
        return env.get_shortest_distance(node.pursuant_state, node.evader_state)

    def construct_children(self, node: Node, env: Environment) -> List[Node]:
        """
        Build child Node objects for `node`, for every legal move of node.agent_role.

        Important: This does *not* mutate the environment. It uses the node's stored
        positions and env.get_neighbors(...) to find legal destination cells.
        """
        children: List[Node] = []

        agent_to_move = node.agent_role
        # determine current position of the moving agent in this node
        if agent_to_move == Role.PURSUANT:
            cur_pos = node.pursuant_state
        else:
            cur_pos = node.evader_state

        # valid destinations around cur_pos (ensures obstacles handled)
        # env.get_neighbors expects a CellIndex and checks bounds/obstacles
        neighbors = env.get_neighbors(cur_pos)

        # If there are no neighbors, return empty list (no legal moves)
        for dest in neighbors:
            # create new positions depending on which agent moved
            if agent_to_move == Role.PURSUANT:
                new_p = dest
                new_e = node.evader_state
            else:
                new_p = node.pursuant_state
                new_e = dest

            # compute distance for child
            dist = env.get_shortest_distance(new_p, new_e)

            child_node = Node(
                depth=max(0, node.depth - 1) if hasattr(node, "depth") else 0,
                agent_role=get_adversary(agent_to_move),  # next to move
                pursuant_state=new_p,
                evader_state=new_e,
                distance=dist,
                children_list=[],
            )
            children.append(child_node)

        # attach children list to the node (optional; helpful for debugging / selecting actions)
        node.children_list = children
        return children

    # Convenience: choose best child (useful when deciding which action to take)
    def choose_action(self, root: Node, lookahead_depth: int, env: Environment):
        """
        Return the child Node with the best minimax value for the agent at `root`.

        Returns:
            (best_child_node, best_value) or (None, None) if no children.
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
        else:  # PURSUANT
            best_value = math.inf
            for child in children:
                val = self.minimax(child, lookahead_depth - 1, env)
                if val is not None and val < best_value:
                    best_value = val
                    best_child = child

        return best_child, best_value
