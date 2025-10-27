from gamestate import GameState

# from visualizations import gamestate_visual
from utils import Role

if __name__ == "__main__":
    results = []
    for episode in range(0, 100):
        game = GameState(episode)
        winner, game_history = game.run_loop()
        results.append(winner)
        # gamestate_gif(episode, game_history)

    print(f"# of pursuant wins: {results.count(Role.PURSUANT)}\n")
    print(f"# of evader wins: {results.count(Role.EVADER)}\n")
    print(f"# of ties: {results.count(None)}\n")
