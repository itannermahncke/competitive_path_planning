from gamestate import GameState
from utils import Role

if __name__ == "__main__":

    results = []
    for episode in range(0, 100):
        game = GameState()
        results.append(game.run_loop())

    print(f"# of pursuant wins: {results.count(Role.PURSUANT)}\n")
    print(f"# of evader wins: {results.count(Role.EVADER)}\n")
    print(f"# of ties: {results.count(None)}\n")
