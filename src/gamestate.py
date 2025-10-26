"""Main"""

from environment import Environment
from minimax import MiniMaxAgent
from utils import Occupancy, CellIndex, Role


class GameState:
    """main"""

    def __init__(
        self,
        size=10,
        density=0.2,
        p_start=CellIndex(0, 0),
        e_start=CellIndex(9, 9),
    ):

        # Initialize robotic agents
        p = Occupancy.PURSUANT
        e = Occupancy.EVADER

        # Initialize an agent of the minimax algorithm
        self.agent = MiniMaxAgent()

        self.env = Environment(size, density, p_start, e_start, p, e)

        self.is_maximizer_turn: Role = Role.MAXIMIZER  # True

        self.move: CellIndex = None
        self.pos: CellIndex = None

    def run_loop(self):
        """
        Constant run loop of alternating game moves.
        """
        print("----------STARTING GAME.-------------")

        # Run game if pursuant has not won
        while not self.env.is_pursuant_win():
            self.next_move()
            self.update_gamestate()

        # TODO: add in logic for evader, game tie

        print("------ GAME OVER. The evader was captured. ------")

    def next_move(self):
        """
        Calls the minimax alg to compute next best move.
        """

        # Alternating turns
        if self.is_maximizer_turn == False:
            self.is_maximizer_turn = Role.MAXIMIZER
            # Get current position of evader agent
            self.pos = self.env.get_agent_cell(Occupancy.EVADER)
        else:
            self.is_maximizer_turn = Role.MINIMIZER  # Pursuer goes first
            # Get current position of pursuant agent
            self.pos = self.env.get_agent_cell(Occupancy.PURSUANT)

        # Compute agent's next move from current positions
        self.move = self.agent._get_next(
            self.env,
            self.pos,
            self.is_maximizer_turn,
        )

    def occupancyToRole(agent: Occupancy) -> Role:
        if agent == Occupancy.EVADER:
            return Role.MAXIMIZER
        elif agent == Occupancy.PURSUANT:
            return Role.MINIMIZER

    def roleToOccupancy(agent: Role) -> Occupancy:
        if agent == Role.MINIMIZER:
            return Occupancy.PURSUANT
        elif agent == Role.MAXIMIZER:
            return Occupancy.EVADER

    def update_gamestate(self):
        """Move agent's location in the environment"""

        print("---------- MOVING AGENT ----------")
        self.env.move_agent(self.pos, self.move)
