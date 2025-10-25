"""Main"""
from environment import Environment
from minimax import MiniMaxAgent
from utils import Occupancy, CellIndex, Role

class GameState:
    """main"""

    def __init__(self, size=10, density=0.2, p_start=CellIndex(0,0), e_start=CellIndex(9,9)):
        
        # Pursuer wants to minimize distance (from Evader)
        self.p = MiniMaxAgent(Occupancy.PURSUANT, Role.MINIMIZER, p_start)
        # Evader wants to maximize distance (from Pursuer)
        self.e = MiniMaxAgent(Occupancy.EVADER, Role.MAXIMIZER, e_start)

        self.env = Environment(size, density, p_start, e_start)

        self.p_move: CellIndex = None
        self.e_move: CellIndex = None

    def run_loop(self):
        if not self.env.is_pursuant_win():
            self.next_move()
            self.update_gamestate
        else:
            print("------ GAME OVER. The evader agent was captured. :,( ------")

    def next_move(self):
        """Calls the minimax alg to compute next best move."""

        # Get current position of agents
        p_loc = self.env.get_agent_cell(Occupancy.PURSUANT)
        e_loc = self.env.get_agent_cell(Occupancy.EVADER)

        # Compute agent's next move from current positions
        self.p_move = self.p.get_next_move(self.env, p_loc, e_loc)
        self.e_move = self.e.get_next_move(self.env, e_loc, p_loc)

    def update_gamestate(self):
        """Call env to move agent after computing"""

        print("---------- MOVING AGENTS ----------")

        # Move agents with best move
        self.env.move_agent(self.p.loc, self.p_move)    
        self.env.move_agent(self.e.loc, self.e_move)
