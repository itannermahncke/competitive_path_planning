"""Main"""

from environment import Environment
from minimax import MiniMax
from utils import CellIndex, Role, Node, get_adversary, derive_action
from visualizations import visualize_game_tree


class GameState:
    """
    Track the game tree and call minimax algorithm to optimally direct agents in the environment.
    """

    def __init__(
        self,
        size=5,
        density=0.2,
        p_start=CellIndex(0, 0),
        e_start=CellIndex(4, 4),
    ):
        # Initialize an instance of the minimax algorithm
        self.agents = MiniMax()

        # Initialize a field to play on
        self.env = Environment(
            size,
            density,
            p_start,
            e_start,
        )

        # Updating game attributes
        self.turn_count = 0
        self.current_turn = Role.PURSUANT  # starts with pursuant
        self.current_agent_pos = None

        # Other tools
        self.EVADER_THRESHOLD = 25
        self.LOOKAHEAD_DEPTH = 3
        self.SMALLEST_DISTANCE = 0
        self.GREATEST_DISTANCE = self.env.size**2
        self.node_id_counter = 0

    def run_loop(self) -> Role:
        """
        Run the game.

        Returns:
            The winner of the game, or None if the game was impossible.
        """
        print("----------STARTING GAME.-------------")
        if (
            self.env.get_shortest_distance(
                self.env.get_agent_cell(Role.PURSUANT),
                self.env.get_agent_cell(Role.EVADER),
            )
            is None
        ):
            print("------ GAME OVER. The field was intraversible. ------")
            return None

        # Run game if pursuant has not won
        while not self.is_pursuant_win() and not self.is_evader_win():
            next_action = self.compute_next_move()
            self.env.move_agent(self.current_turn, next_action)
            self.switch_turns()

        if self.is_pursuant_win():
            print("------ GAME OVER. The evader was captured. ------")
            return Role.PURSUANT
        else:
            print("------ GAME OVER. The evader escaped. ------")
            return Role.EVADER

    def switch_turns(self):
        """
        Hand over state variables to the opponent.
        """
        self.current_turn = get_adversary(self.current_turn)
        self.current_agent_pos = self.env.get_agent_cell(self.current_turn)
        self.turn_count += 1

    def compute_next_move(self):
        """
        Calls the minimax algorithm to compute best move.
        """
        print(f"T{self.turn_count}) Agent {self.current_turn}\n")
        # build tree of possible actions
        root_node: Node = self.build_game_tree(self.current_turn)
        visualize_game_tree(root_node, self.current_turn)

        # prepare to find the best action
        best_child: Node = None
        best_distance = None
        if self.current_turn == Role.EVADER:
            best_distance = self.SMALLEST_DISTANCE
        else:
            best_distance = self.GREATEST_DISTANCE

        # call the minimax algorithm on each child to find the best choice
        for n in root_node.children:
            # calculate and report the heuristic value
            distance = self.agents.minimax(
                node=n,
                depth=self.LOOKAHEAD_DEPTH,
                alpha=self.SMALLEST_DISTANCE,
                beta=self.GREATEST_DISTANCE,
            )
            print(f"-> child {n.action_from_parent} has value {distance}")
            if (distance > best_distance and self.current_turn == Role.EVADER) or (
                distance < best_distance and self.current_turn == Role.PURSUANT
            ):
                best_child = n
                best_distance = distance

        # return the action required to move from the root state to the best possible next state
        print(f"-> chose {best_child.action_from_parent}\n")
        return best_child.action_from_parent

    def build_game_tree(self, initial_state: Role) -> Node:
        """
        Calculate all possible game states until the look-ahead depth is reached.

        Args:
            initial_state (Role): indicates who's turn it is at the root node

        Returns:
            The root node of the game tree, from which the rest of the tree can be accessed.
        """
        # reset node counter
        self.node_id_counter = 0
        # build the root node
        p_pos = self.env.get_agent_cell(Role.PURSUANT)
        e_pos = self.env.get_agent_cell(Role.EVADER)
        root = Node(
            id=self.node_id(),
            depth=0,
            agent_role=initial_state,
            pursuant_state=p_pos,
            evader_state=e_pos,
            distance=self.env.get_shortest_distance(
                p_pos,
                e_pos,
            ),
            action_from_parent=None,
            parent=None,
            children=[],
        )

        # expand children recursively
        self.construct_node_children(root)

        # return root
        return root

    def construct_node_children(self, parent: Node):
        """
        Recursively construct each node's child in an expansion of the game tree.

        Args:
            node (Node): the node to expand
        """
        # break if at depth
        if parent.depth >= self.LOOKAHEAD_DEPTH:
            return

        # find all children of this game state given agent
        if parent.agent_role == Role.PURSUANT:
            children = self.env.get_neighbors(parent.pursuant_state)
        else:
            children = self.env.get_neighbors(parent.evader_state)

        # construct the children
        for neighbor_cell in children:
            # locate agents in new state and figure out what happened
            p_pos = None
            e_pos = None
            action_taken = None
            if parent.agent_role == Role.PURSUANT:
                p_pos = neighbor_cell
                e_pos = parent.evader_state
                action_taken = derive_action(
                    parent.pursuant_state,
                    neighbor_cell,
                )
            else:
                p_pos = parent.pursuant_state
                e_pos = neighbor_cell
                action_taken = derive_action(
                    parent.evader_state,
                    neighbor_cell,
                )

            # construct the child
            child_node = Node(
                id=self.node_id(),
                depth=parent.depth + 1,
                agent_role=get_adversary(parent.agent_role),
                pursuant_state=p_pos,
                evader_state=e_pos,
                distance=self.env.get_shortest_distance(
                    p_pos,
                    e_pos,
                ),
                action_from_parent=action_taken,
                parent=parent,
                children=[],
            )

            # attach and expand the child
            parent.children.append(child_node)
            self.construct_node_children(child_node)

    def node_id(self):
        self.node_id_counter += 1
        return self.node_id_counter

    def is_pursuant_win(self):
        """
        Check and return if the pursuant has captured the evader.

        Returns:
            True if so, False otherwise.
        """
        return self.env.is_agent_adjacent()

    def is_evader_win(self):
        """
        Check and return if the evader has suffiently survived.

        Returns:
            True if so, False otherwise.
        """
        return self.turn_count >= self.EVADER_THRESHOLD
