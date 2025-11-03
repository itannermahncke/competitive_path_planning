from gamestate import GameState

from visualizations import gamestate_gif
from utils import Role

if __name__ == "__main__":
    results = []
    for episode in range(0, 20):
        game = GameState(episode)
        winner, game_history = game.run_loop()
        results.append(winner)

        if episode <= 0:
            gamestate_gif(0)

    print(f"# of pursuant wins: {results.count(Role.PURSUANT)}\n")
    print(f"# of evader wins: {results.count(Role.EVADER)}\n")
    print(f"# of ties: {results.count(None)}\n")
