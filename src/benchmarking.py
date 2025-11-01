"""Compare different game outcomes when adjusting initializing parameters."""

from gamestate import GameState
from utils import Role
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time


def density_sweep(n, density_vals):
    """
    Parameter sweep of obstacle density in environment formation.
    """
    density_results = []
    for val in density_vals:
        print(f"CURRENT DENSITY IS: {val}")
        result = []
        for trial in range(n):
            game = GameState(episode=trial, density=val)
            winner = game.run_loop()
            print(f"WINNER IS {winner}")
            result.append(winner)
        density_results.append(result)
    return density_results


def map_size_sweep(n, size_vals):
    """
    Parameter sweep of map size in environment formation.
    """
    size_results = []
    for val in size_vals:
        print(f"CURRENT MAP SIZE IS: {val}")
        result = []
        for trial in range(n):
            game = GameState(episode=trial, size=val)
            winner = game.run_loop()
            print(f"WINNER IS {winner}")
            result.append(winner)
        size_results.append(result)
    return size_results


def depth_sweep(n, depth_vals):
    """
    Parameter sweep of look-ahead depth.
    """
    depth_results = []
    for val in depth_vals:
        print(f"CURRENT DEPTH IS: {val}")
        result = []
        for trial in range(n):
            game = GameState(episode=trial, depth=val)
            winner = game.run_loop()
            print(f"WINNER IS {winner}")
            result.append(winner)
        depth_results.append(result)
    return depth_results


def pruning_comparison(n, depth_vals):
    """
    Compare outcomes and performance between alpha-beta and plain minimax.
    """
    from minimax_ab import MiniMax as MiniMaxNoPrune
    from minimax_ab import MiniMax as MiniMaxAB  # rename your alpha-beta file to minimax_ab.py

    results = []
    for depth in depth_vals:
        print(f"Testing depth {depth}")
        ab_times, plain_times = [], []
        ab_winners, plain_winners = [], []

        for trial in range(n):
            # Run alpha-beta version
            t0 = time.time()
            game_ab = GameState(episode=trial, depth=depth, minimax_class=MiniMaxAB)
            ab_winner = game_ab.run_loop()
            ab_times.append(time.time() - t0)
            ab_winners.append(ab_winner)

            # Run plain minimax version
            t1 = time.time()
            game_plain = GameState(episode=trial, depth=depth, minimax_class=MiniMaxNoPrune)
            plain_winner = game_plain.run_loop()
            plain_times.append(time.time() - t1)
            plain_winners.append(plain_winner)

        results.append({
            "depth": depth,
            "ab_avg_time": np.mean(ab_times),
            "plain_avg_time": np.mean(plain_times),
            "ab_pursuer_wins": ab_winners.count(Role.PURSUANT),
            "ab_evader_wins": ab_winners.count(Role.EVADER),
            "plain_pursuer_wins": plain_winners.count(Role.PURSUANT),
            "plain_evader_wins": plain_winners.count(Role.EVADER),
        })

    return pd.DataFrame(results)


def create_bar_chart(parameter_vals, results, parameter_name):
    """
    Visualize win rates for a parameter sweep.
    """
    pursuer_win_rate = [r.count(Role.PURSUANT) / len(r) for r in results]
    evader_win_rate = [r.count(Role.EVADER) / len(r) for r in results]
    tie_rate = [r.count(None) / len(r) for r in results]

    bar_width = 0.25
    bar_spacing = 0.1
    x_positions = np.arange(len(parameter_vals)) * (bar_width + bar_spacing)

    plt.figure(figsize=(8, 5))
    plt.bar(x_positions, pursuer_win_rate, bar_width, color='r', label='Pursuer')
    plt.bar(x_positions, evader_win_rate, bar_width, bottom=pursuer_win_rate, color='g', label='Evader')
    plt.bar(x_positions, tie_rate, bar_width, bottom=np.array(pursuer_win_rate) + np.array(evader_win_rate), color='k', label='Tie')

    plt.xticks(x_positions, [str(d) for d in parameter_vals])
    plt.xlabel(parameter_name)
    plt.ylabel("Proportion of Outcomes")
    plt.title(f"Win Rate Distribution by {parameter_name}")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_pruning_comparison(df):
    """
    Plot timing comparison between pruning and non-pruning minimax.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(df["depth"], df["plain_avg_time"], 'o-', label="No Pruning")
    plt.plot(df["depth"], df["ab_avg_time"], 'o-', label="Alpha-Beta")
    plt.xlabel("Search Depth")
    plt.ylabel("Average Runtime (s)")
    plt.title("Alpha-Beta vs Non-Pruning Minimax Performance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    n = 10  # trials per test
    depth_vals = [1, 2, 3, 4]
    df = pruning_comparison(n, depth_vals)
    print(df)
    plot_pruning_comparison(df)
