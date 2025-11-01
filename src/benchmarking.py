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
