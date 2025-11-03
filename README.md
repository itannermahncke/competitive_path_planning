# Competitive Path Planning With Alpha-Beta Pruning
> **MTH 2110 Discrete Math:** Combinatorics and Graph Theory
**Contributors:** Irene Hong, Ivy Mahncke, Vivian Mak

!["game demo"](https://github.com/itannermahncke/competitive_path_planning/blob/main/docs/gamestate_gifs/game_0.gif)

## Project Overview
For this project, we implemented the minimax algorithm with alpha-beta pruning to optimize two competing mobile robots in a pursuer-evader game.

To read our final report, including methodology and results, [please check out this document!](https://github.com/itannermahncke/competitive_path_planning/blob/main/docs/report.pdf)

In the game, two robotic agents traverse an obstacle-dense graph world: the first seeks to minimize the distance between the two, while the second seeks to maximize that distance. Their actions (up, down, left, and right) will be chosen by the minimax algorithm, which alternately selects actions that minimize or maximize the distance between the agents. The minimax algorithm models the game state as an m-ary tree (m = 4), in which each node represents a game state and its children are the next possible game states. The alpha-beta pruning optimization method simplifies the tree by “looking ahead” to future game states and pre-emptively eliminating branches that do not contain a better outcome for the current agent.

The world itself is discretized as an occupancy grid, structured as a two-dimensional array. Every call is adjacent to at most four other cells (up, down, left, right), but can be adjacent to less if on the edge of the world. Cells containing obstacles contain a value of -1 and are impassable. Cells occupied by an agent contain a 1. All other cells contain a zero. We will explore how obstacle density in the world influences the results in the game.

To win the game, the pursuant must be in a node adjacent to the evader’s current node. If the evader successfully avoids the pursuant for a certain number of turns, it wins instead.

## Package Structure

Our initial project proposal and final project report can be found in `docs`.

Our codebase, including the environment simulator, minimax algorithm, and visualization code, can be found in `src`.

All relevant unit tests can be found in `test`.

```bash
├── docs
│   ├── game_trees
│   ├── gamestate_gifs
│   ├── proposal.pdf
│   ├── report.pdf
├── src
│   ├── __init__.py
│   ├── simple_run.py
│   ├── environment.py
│   ├── minimax.py
│   ├── gamestate.py
│   ├── benchmarking.py
│   ├── visualizations.py
│   ├── utils.py
├── test
│   ├── __init__.py
│   ├── test_environment.py
│   ├── test_utils.py
├── requirements.txt
├── .gitignore
├── README.md
```

## How To Run

First, clone the repository onto your machine:
```
git clone git@github.com:itannermahncke/competitive_path_planning.git
```

Next, download the package dependencies:
```
pip install -r requirements.txt.
```

Finally, run `simple_run.py` for a console-based demo of the algorithm in action.

## Resources
- Primer on Minimax and AB Pruning https://www.geeksforgeeks.org/artificial-intelligence/mini-max-algorithm-in-artificial-intelligence/
- Understanding the Minimax Algorithm w/ AB Pruning https://www.youtube.com/watch?v=l-hh51ncgDI
- Creating the environment visuals https://stackoverflow.com/questions/56614725/generate-grid-cells-occupancy-grid-color-cells-and-remove-xlabels 
