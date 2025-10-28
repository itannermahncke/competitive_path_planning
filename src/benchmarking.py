"""Compare different game outcomes when adjusting initializaing paramaters."""

from gamestate import GameState
from utils import Role
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def density_sweep(n, density_vals):
    """
    Parameter sweep of obstacle density in environment formation.
    
    Args:
        n (int): episodes of game
        density_vals (list of ints): parameter values to be tested

    Returns:
        List of lists representing winners per game episode for every parameter value. 
    """
    density_results = []
    for val in density_vals:
        print(f"CURRENT DENSTIY IS: {val}")
        result = []
        for trial in range(n):
            game = GameState(episode=trial, depth=val)
            winner = game.run_loop() 
            print(f"WINNER IS {winner}")
            result.append(winner)
        density_results.append(result)

    return density_results


def map_size_sweep(n, size_vals):
    """
    Parameter sweep of map size in environment formation.
    
    Args:
        n (int): episodes of game
        size_vals (list of ints): parameter values to be tested

    Returns:
        List of lists representing winners per game episode for every parameter value. 
    """
    size_results = []
    for val in size_vals:
        print(f"CURRENT DENSTIY IS: {val}")
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
    Parameter sweep of look-ahead depth in AB Pruning.
    
    Args:
        n (int): episodes of game
        depth_vals (list of ints): parameter values to be tested

    Returns:
        List of lists representing winners per game episode for every parameter value. 
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


def create_bar_chart(n, parameter):
    """
    Create a bar chart visualizing a given parameter sweep for a certain number of trials for each parameter value.

    Args:
        n (int): episodes of game
        parameter (str): parameter to be tested

    Returns:
        A bar chart. 
    """
    # Number of games run per density
    n = 100

    # Win Rates
    pursuer_win_rate = []
    evader_win_rate = []
    tie_rate = []

    parameter_vals = []
    # Parameter sweep values
    if parameter == "Obstacle Density":
        vals = range(0,1,0.1)
    elif parameter == "Map Size":
        vals = range(5, 100)
    elif parameter == "Look-Ahead Depth":
        vals = range(1,25)

    for val in parameter_vals:
        pursuer_win_rate.append(val.count(Role.PURSUANT))
        evader_win_rate.append(val.count(Role.EVADER))
        tie_rate.append(val.count(None))


    # Convert counts to proportions
    total_games = np.array(pursuer_win_rate) + np.array(evader_win_rate) + np.array(tie_rate)
    pursuer_rate = np.array(pursuer_win_rate) / total_games
    evader_rate = np.array(evader_win_rate) / total_games
    tie_rate = np.array(tie_rate) / total_games

    # Add spacing between bars
    bar_width = 0.25
    bar_spacing = 0.1
    x_positions = np.arange(len(parameter_vals)) * (bar_width + bar_spacing)

    # Plot stacked bars
    plt.figure(figsize=(8, 5))
    plt.bar(x_positions, pursuer_rate, bar_width, color='r', label='Pursuer')
    plt.bar(x_positions, evader_rate, bar_width, bottom=pursuer_rate, color='g', label='Evader')
    plt.bar(x_positions, tie_rate, bar_width, bottom=pursuer_rate + evader_rate, color='k', label='Tie')

    # Axis labels and formatting
    plt.xticks(x_positions, [str(d) for d in parameter_vals])
    plt.xlabel(parameter)
    plt.ylabel("Proportion of Outcomes")
    plt.title(f"Stacked Win Rate Distribution by {parameter}")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

        
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
