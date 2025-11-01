"""gamestate.py — main game loop and game-tree builder (supports both minimax_ab and minimax)"""

from environment import Environment
from utils import CellIndex, Role, Node, get_adversary, derive_action
from typing import Optional, List

# You can switch between the two algorithms here:
from minimax_ab import MiniMax  # alpha-beta pruning version
from minimax import MiniMax        # basic minimax version (no alpha-beta)


class GameState:
    """
    Track the game tree and call minimax algorithm to optimally direct agents in the environment.
    """

    def __init__(
        self,
        episode,
        size=5,
        density=0.2,
        depth=3,
        p_start=CellIndex(0, 0),
        e_start=CellIndex(4, 4),
        minimax_class=None,   # ✅ NEW PARAM — allows switching algorithm dynamically
    ):
        # pick which minimax implementation to use
        if minimax_class is not None:
            self.agents = minimax_class()
        else:
            from minimax import MiniMax  # fallback default (non-pruned)
            self.agents = MiniMax()

        # Initialize the environment
        self.env = Environment(
            size,
            density,
            p_start,
            e_start,
        )

        # Updating game attributes
        self.episode = episode
        self.turn_count = 0
        self.current_turn = Role.PURSUANT  # starts with pursuant
        self.current_agent_pos = None
        self.game_history = []

        # Other tools / constants
        self.EVADER_THRESHOLD = 25
        self.LOOKAHEAD_DEPTH = depth
        self.SMALLEST_DISTANCE = 0
        self.GREATEST_DISTANCE = self.env.size**2
        self.node_id_counter = 0

    def run_loop(self) -> tuple[Optional[Role], list]:
        """
        Run the game.
        Returns the winner (Role) or None if impossible, and the game history (list).
        """
        print(f"---------- STARTING GAME #{self.episode} ----------")

        # If field is intraversible, end immediately
        if (
            self.env.get_shortest_distance(
                self.env.get_agent_cell(Role.PURSUANT),
                self.env.get_agent_cell(Role.EVADER),
            )
            is None
        ):
            print("------ GAME OVER. The field was intraversible. ------")
            return (None, self.game_history)

        self.game_history.append(self.env._graph.copy())

        while not self.is_pursuant_win() and not self.is_evader_win():
            next_action = self.compute_next_move()
            if next_action is None:
                print("No valid move could be computed; ending game.")
                return (None, self.game_history)

            moved = self.env.move_agent(self.current_turn, next_action)
            if not moved:
                print("Attempted illegal move; ending game.")
                return (None, self.game_history)

            self.switch_turns()

        if self.is_pursuant_win():
            print("------ GAME OVER. The evader was captured. ------")
            return (Role.PURSUANT, self.game_history)
        else:
            print("------ GAME OVER. The evader escaped. ------")
            return (Role.EVADER, self.game_history)

    def switch_turns(self):
        """Switch active agent and update internal state."""
        self.game_history.append(self.env._graph.copy())
        self.current_turn = get_adversary(self.current_turn)
        self.current_agent_pos = self.env.get_agent_cell(self.current_turn)
        self.turn_count += 1

    def compute_next_move(self):
        """Call minimax (with or without alpha-beta pruning) to compute best move."""
        print(f"T{self.turn_count}) Agent {self.current_turn}\n")
        root_node = self.build_game_tree(self.current_turn)
        self.construct_node_children(root_node)

        if not root_node.children_list:
            valid_moves = self.env.get_valid_moves(self.current_turn)
            if not valid_moves:
                print("No valid moves for current agent.")
                return None
            fallback_dest = valid_moves[0]
            cur_pos = (
                self.env.get_agent_cell(Role.PURSUANT)
                if self.current_turn == Role.PURSUANT
                else self.env.get_agent_cell(Role.EVADER)
            )
            action = derive_action(cur_pos, fallback_dest)
            print(f"No children; fallback move: {action}")
            return action

        best_child = None
        best_distance = (
            self.SMALLEST_DISTANCE
            if self.current_turn == Role.EVADER
            else self.GREATEST_DISTANCE
        )

        # --- Unified call signature for both minimax versions ---
        for n in root_node.children_list:
            if "alpha" in MiniMax.minimax.__code__.co_varnames:
                # alpha-beta version
                distance = self.agents.minimax(
                    node=n,
                    depth=self.LOOKAHEAD_DEPTH - 1,
                    env=self.env,
                    alpha=self.SMALLEST_DISTANCE,
                    beta=self.GREATEST_DISTANCE,
                )
            else:
                # plain minimax (no alpha-beta)
                distance = self.agents.minimax(
                    node=n,
                    depth=self.LOOKAHEAD_DEPTH - 1,
                    env=self.env,
                )

            print(f"-> child {getattr(n, 'action_from_parent', None)} = {distance}")

            if distance is None:
                continue

            if (distance > best_distance and self.current_turn == Role.EVADER) or (
                distance < best_distance and self.current_turn == Role.PURSUANT
            ):
                best_child = n
                best_distance = distance

        if not best_child and root_node.children_list:
            best_child = root_node.children_list[0]
            print("All minimax results invalid; picking first child as fallback.")
        elif not best_child:
            print("No valid children; returning None.")
            return None

        print(f"-> chose {best_child.action_from_parent}\n")
        return best_child.action_from_parent

    def build_game_tree(self, initial_state: Role) -> Node:
        """Builds root node for current environment."""
        p_pos = self.env.get_agent_cell(Role.PURSUANT)
        e_pos = self.env.get_agent_cell(Role.EVADER)
        root = Node(
            depth=0,
            agent_role=initial_state,
            pursuant_state=p_pos,
            evader_state=e_pos,
            distance=self.env.get_shortest_distance(p_pos, e_pos),
            children_list=[],
        )
        root.action_from_parent = None
        root.parent = None
        root.id = self.node_id()
        return root

    def construct_node_children(self, parent: Node):
        """Recursively build all possible next moves."""
        if parent.depth >= self.LOOKAHEAD_DEPTH:
            return

        neighbor_cells = (
            self.env.get_neighbors(parent.pursuant_state)
            if parent.agent_role == Role.PURSUANT
            else self.env.get_neighbors(parent.evader_state)
        )

        for neighbor_cell in neighbor_cells:
            if parent.agent_role == Role.PURSUANT:
                p_pos, e_pos = neighbor_cell, parent.evader_state
                action_taken = derive_action(parent.pursuant_state, neighbor_cell)
            else:
                p_pos, e_pos = parent.pursuant_state, neighbor_cell
                action_taken = derive_action(parent.evader_state, neighbor_cell)

            child = Node(
                depth=parent.depth + 1,
                agent_role=get_adversary(parent.agent_role),
                pursuant_state=p_pos,
                evader_state=e_pos,
                distance=self.env.get_shortest_distance(p_pos, e_pos),
                children_list=[],
            )
            child.action_from_parent = action_taken
            child.parent = parent
            child.id = self.node_id()
            parent.children_list.append(child)
            self.construct_node_children(child)

    def node_id(self):
        self.node_id_counter += 1
        return self.node_id_counter

    def is_pursuant_win(self):
        return self.env.is_agent_adjacent()

    def is_evader_win(self):
        return self.turn_count >= self.EVADER_THRESHOLD
