"""Compare different game outcomes when adjusting initializaing paramaters."""

from gamestate import GameState
from utils import Role
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def density_sweep(n, density_vals):
    """"""
    density_results = []
    for d in density_vals:
        print(f"CURRENT DESNTIY IS: {d}")
        result = []
        for _ in range(n):
            game = GameState(density=d)
            r = game.run_loop()
            print(f"WINNER IS {r}")
            result.append(r)
        density_results.append(result)

    return density_results


def map_size_sweep():
    pass


def depth_sweep():
    pass


if __name__ == "__main__":

    # Number of games run per density
    n = 100

    # Win Rates
    pursuer_win_rate = []
    evader_win_rate = []
    tie_rate = []

    # Density sweep values
    density_vals = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    density_results = density_sweep(n, density_vals)
    # print("THE DENSITY RESULTS ARE:")
    # print(density_results)

    for d in density_results:
        pursuer_win_rate.append(d.count(Role.PURSUANT))
        evader_win_rate.append(d.count(Role.EVADER))
        tie_rate.append(d.count(None))


    # Convert counts to proportions
    total_games = np.array(pursuer_win_rate) + np.array(evader_win_rate) + np.array(tie_rate)
    pursuer_rate = np.array(pursuer_win_rate) / total_games
    evader_rate = np.array(evader_win_rate) / total_games
    tie_rate = np.array(tie_rate) / total_games

    # Add spacing between bars
    bar_width = 0.25
    bar_spacing = 0.1
    x_positions = np.arange(len(density_vals)) * (bar_width + bar_spacing)

    # Plot stacked bars
    plt.figure(figsize=(8, 5))
    plt.bar(x_positions, pursuer_rate, bar_width, color='r', label='Pursuer')
    plt.bar(x_positions, evader_rate, bar_width, bottom=pursuer_rate, color='g', label='Evader')
    plt.bar(x_positions, tie_rate, bar_width, bottom=pursuer_rate + evader_rate, color='k', label='Tie')

    # Axis labels and formatting
    plt.xticks(x_positions, [str(d) for d in density_vals])
    plt.xlabel("Obstacle Density")
    plt.ylabel("Proportion of Outcomes")
    plt.title("Stacked Win Rate Distribution by Density")
    plt.legend()
    plt.tight_layout()
    plt.show()

        
    # Heat map
    # df = pd.DataFrame({
    #     "density": density_vals,
    #     "pursuer_win_rate": density_results.count(Role.MINIMIZER),
    #     "evader_win_rate": density_results.count(Role.MAXIMIZER),
    #     "tie_rate": density_results.count(None),
    # })

    # plt.bar(density_vals, density_results, co)

    # df = pd.DataFrame({
    #     "density": density_vals,
    #     "pursuer_win_rate": 0.4,
    #     "evader_win_rate": 0.5,
    #     "tie_rate": 0.1,
    # })
    
    # df_melted = df.melt(id_vars="density", var_name="Outcome", value_name="Win Rate")
    # heat_data = df_melted.pivot(index="Outcome", columns="density", values="Win Rate")

    # plt.figure(figsize=(10, 4))
    # sns.heatmap(heat_data, annot=True, cmap="coolwarm", cbar_kws={'label': 'Win Rate'})
    # plt.title("Game Outcomes vs. Obstacle Density")
    # plt.xlabel("Obstacle Density")
    # plt.ylabel("Outcome Type")
    # plt.show()
