"""Compare different game outcomes when adjusting initializaing paramaters."""

from gamestate import GameState
from utils import Role
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run_sweep(n, density_vals, depth_vals):
    """"""
    results = []
    for d in density_vals:
        for depth in depth_vals:
            print(f"RUNNING DESNTIY={d} AND DEPTH={depth}")
            result = []
            for i in range(n):
                game = GameState(episode=i, depth=depth, density=d)
                r = game.run_loop()
                # print(f"WINNER IS {r[0]}")
                result.append(r[0])
            # Count outcomes
            total = len(result)
            pursuer_wins = result.count(Role.PURSUANT) / total
            evader_wins = result.count(Role.EVADER) / total
            ties = result.count(None) / total

            # Record results
            results.append({
                "density": d,
                "depth": depth,
                "pursuer_win_rate": pursuer_wins,
                "evader_win_rate": evader_wins,
                "tie_rate": ties
            })

    return pd.DataFrame(results)


if __name__ == "__main__":

    # Number of games run per density
    n = 100

    # Density sweep values
    density_vals = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    depth_vals = [3, 4, 5, 6]

    results = run_sweep(n, density_vals, depth_vals)
    print(results.head())
    
    # Create heatmaps for each outcome
    outcomes = ["pursuer_win_rate", "evader_win_rate", "tie_rate"]
    titles = ["Pursuer Win Rate", "Evader Win Rate", "Tie Rate"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, (metric, title) in enumerate(zip(outcomes, titles)):
        heat_data = results.pivot(index="depth", columns="density", values=metric)
        sns.heatmap(
            heat_data,
            ax=axes[i],
            annot=True,
            cmap="coolwarm",
            vmin=0,
            vmax=1,
            cbar_kws={'label': 'Win Rate'}
        )
        axes[i].set_title(title)
        axes[i].set_xlabel("Density")
        axes[i].set_ylabel("Lookahead Depth")

    plt.tight_layout()
    plt.show()



    

    # # ~~~~~~~~~
    # # print("THE DENSITY RESULTS ARE:")
    # # print(density_results)

    # # for d in density_results:
    # #     pursuer_win_rate.append(d.count(Role.PURSUANT))
    # #     evader_win_rate.append(d.count(Role.EVADER))
    # #     tie_rate.append(d.count(None))


    # # Convert counts to proportions
    # # total_games = n * len(density_vals)
    # total_games = np.array(pursuer_win_rate) + np.array(evader_win_rate) + np.array(tie_rate)
    # pursuer_rate = np.array(pursuer_win_rate) / total_games
    # evader_rate = np.array(evader_win_rate) / total_games
    # tie_rate = np.array(tie_rate) / total_games

    # # Add spacing between bars
    # bar_width = 0.25
    # bar_spacing = 0.1
    # x_positions = np.arange(len(density_vals)) * (bar_width + bar_spacing)

    # # Plot stacked bars
    # plt.figure(figsize=(8, 5))
    # plt.bar(x_positions, pursuer_rate, bar_width, color='r', label='Pursuer')
    # plt.bar(x_positions, evader_rate, bar_width, bottom=pursuer_rate, color='g', label='Evader')
    # plt.bar(x_positions, tie_rate, bar_width, bottom=pursuer_rate + evader_rate, color='k', label='Tie')

    # # Axis labels and formatting
    # plt.xticks(x_positions, [str(d) for d in density_vals])
    # # plt.xlabel("Obstacle Density")
    # plt.xlabel("Look Ahead Depth")
    # plt.ylabel("Proportion of Win Rates")
    # plt.title("Win Rate Distribution by Search Depth (Out of 100 Games)")
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

        
    # # Heat map
    # # df = pd.DataFrame({
    # #     "density": density_vals,
    # #     "pursuer_win_rate": density_results.count(Role.MINIMIZER),
    # #     "evader_win_rate": density_results.count(Role.MAXIMIZER),
    # #     "tie_rate": density_results.count(None),
    # # })

    # # plt.bar(density_vals, density_results, co)

    # # df = pd.DataFrame({
    # #     "density": density_vals,
    # #     "pursuer_win_rate": 0.4,
    # #     "evader_win_rate": 0.5,
    # #     "tie_rate": 0.1,
    # # })
    
    # # df_melted = df.melt(id_vars="density", var_name="Outcome", value_name="Win Rate")
    # # heat_data = df_melted.pivot(index="Outcome", columns="density", values="Win Rate")

    # # plt.figure(figsize=(10, 4))
    # # sns.heatmap(heat_data, annot=True, cmap="coolwarm", cbar_kws={'label': 'Win Rate'})
    # # plt.title("Game Outcomes vs. Obstacle Density")
    # # plt.xlabel("Obstacle Density")
    # # plt.ylabel("Outcome Type")
    # # plt.show()
