# Vacuum Cleaner Agent Simulation Documentation

This program simulates a vacuum cleaner agent operating in a 2D environment. The simulation includes an environment with dirt accumulation, an agent that moves and cleans, and a graphical user interface to visualize and control the simulation.

## Main Components

1. Environment
2. Agent
3. RandomNumberGenerator
4. Evaluator
5. GUI

### Environment Class

The `Environment` class represents the 2D world in which the agent operates.

#### Key attributes:

- `MAZE_SIZE`: Size of the environment (10x10 grid)
- `OBSTACLE`: Constant representing obstacles (-1)
- `maze_`: 2D list representing the environment state
- `agentPosX_`, `agentPosY_`: Agent's current position
- `dirtyProb_`: Probability of a cell becoming dirty in each time step
- `randomSeed_`: Seed for random number generation

#### Key methods:

- `__init__(self, infile)`: Initializes the environment from a map file
- `Change(self, rng)`: Updates the environment, potentially adding dirt to cells
- `AcceptAction(self, action)`: Processes the agent's action, updating its position or cleaning dirt
- `DirtAmount(self, x, y)`: Returns the amount of dirt at a given position
- `isCurrentPosDirty()`: Checks if the agent's current position is dirty
- `isJustBump()`: Checks if the agent just bumped into an obstacle

### Agent Class

The `Agent` class represents the vacuum cleaner agent.

#### Key attributes:

- `ActionType`: Enum-like class defining possible actions (UP, DOWN, LEFT, RIGHT, SUCK, IDLE)
- `bump_`: Boolean indicating if the agent bumped into an obstacle
- `dirty_`: Boolean indicating if the current position is dirty

#### Key methods:

- `Perceive(self, env)`: Updates the agent's perception of the environment
- `Think(self)`: Decides the next action based on current perceptions

### RandomNumberGenerator Class

A simple wrapper for Python's random number generator, ensuring consistent random number generation across runs.

#### Key method:

- `random(self)`: Returns a random float between 0 and 1

### Evaluator Class

The `Evaluator` class calculates and tracks the performance metrics of the agent.

#### Key attributes:

- `dirtyDegree_`: Measure of overall dirtiness of the environment
- `consumedEnergy_`: Amount of energy consumed by the agent

#### Key method:

- `Eval(self, action, env)`: Updates performance metrics based on the agent's action and environment state

### GUI Class

The `GUI` class manages the graphical user interface and simulation control.

#### Key attributes:

- `canvas`: Tkinter canvas for displaying the environment
- `env`, `agent`, `evaluator`, `rng`: Instances of the main simulation components
- Various labels for displaying statistics

#### Key methods:

- `new_map(self)`: Prompts user to select a new map file
- `load_map(self, file_path)`: Loads a map file and initializes the simulation
- `do_one_step(self)`: Performs one step of the simulation
- `do_one_run(self)`: Runs the simulation for one complete lifecycle
- `do_all_run(self)`: Performs multiple runs and calculates average performance
- `update_display(self)`: Updates the graphical display and statistics

## Simulation Flow

1. The user loads a map file, which initializes the environment, agent, and evaluator.
2. The simulation proceeds in steps:
   a. The environment potentially adds dirt to cells.
   b. The agent perceives its surroundings.
   c. The agent decides on an action.
   d. The environment processes the agent's action.
   e. The evaluator updates performance metrics.
   f. The display is updated to reflect the new state.
3. This process continues until the specified lifetime is reached.
4. Multiple runs can be performed to calculate average performance metrics.

## Visualization

- The environment is displayed as a 10x10 grid.
- Obstacles are shown in gray.
- Dirt levels are represented by shades of green (white for clean, dark green for very dirty).
- The agent is represented by a red circle.

## User Interface

The GUI provides buttons for:

- Loading a new map
- Performing one step of the simulation
- Running one complete lifecycle
- Performing multiple runs

Statistics are displayed and updated in real-time, showing:

- Current time step
- Last action taken
- Current dirty degree
- Energy consumed
- Completed runs
- Total and average scores

This simulation allows users to observe and evaluate different strategies for the vacuum cleaner agent in various environment configurations.
