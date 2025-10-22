# Competitive Path Planning With Alpha-Beta Pruning
> **MTH 2110 Discrete Math:** Combinatorics and Graph Theory
**Contributors:** Irene Hong, Ivy Mahncke, Vivian Mak

## Project Overview
For this project, we plan to implement the minimax algorithm with alpha-beta pruning to optimize two competing path planners in a pursuer-evader game.

In the game, two robotic agents traverse an obstacle-dense graph world: the first seeks to minimize the distance between the two, while the second seeks to maximize that distance. Their actions (up, down, left, and right) will be chosen by the minimax algorithm, which alternately selects actions that minimize or maximize the distance between the agents. The minimax algorithm models the game state as an m-ary tree (m = 4), in which each node represents a game state and its children are the next possible game states. The alpha-beta pruning optimization method simplifies the tree by “looking ahead” to future game states and pre-emptively eliminating branches that guarantee a loss for the current agent.

The world itself is discretized as an occupancy grid, structured as a two-dimensional array. Every call is adjacent to at most four other cells (up, down, left, right), but can be adjacent to less if on the edge of the world. Cells containing obstacles contain a value of -1 and are impassable. Cells occupied by an agent contain a 1. All other cells contain a zero. We will explore how obstacle density in the world influences the results in the game.

To win the game, the pursuant must be in a node adjacent to the evader’s current node. If the evader successfully avoids the pursuant for a certain number of turns, it wins instead.


## Package Structure

```Python


```
## Design Decisions
### Agents
Each agent (pursuer and evader) are separate instances of the MiniMaxAgent class. We want agents to use minimax logic to plan indepenently, as opposed to a centralized search that alternates turn internally. This forces the algorithm to constantly compute similarly to real-time since taking turns doesn't exist. Each agent's action is computed for the next timestep without knowing where the other agent will end up.


## How To Run
```

```