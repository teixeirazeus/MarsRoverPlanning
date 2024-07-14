![banner](https://raw.githubusercontent.com/teixeirazeus/MarsRoverPlanning/master/readme_assets/Marsrover-Header.jpg)

# Mars Rover Planning Problem
This project implements a planning problem for a Mars Rover using STRIPS-style representations. The problem involves a rover on Mars that needs to perform several tasks such as collecting samples, taking photos, analyzing rocks and soil, and transmitting data. The goal is to find a sequence of actions that the rover can perform to achieve all these tasks.

## Problem Description
The Mars Rover needs to:

1. Collect a sample from Location1.
2. Take a photo at Location2.
3. Analyze a rock at Location2.
4. Analyze soil at Location1.
5. Transmit the collected data.

## Initial State
- The rover starts at the base.
- The sample is available at Location1.
- There is a photo opportunity at Location2.
- A rock is available for analysis at Location2.
- Soil is available for analysis at Location1.
- No sample is collected.
- No photo is taken.
- No data is transmitted.
- No rock is analyzed.
- No soil is analyzed.

## Goals
- The sample is collected.
- The photo is taken.
- The data is transmitted.
- The rock is analyzed.
- The soil is analyzed.

## Actions

The following actions are defined for the Mars Rover:

1. Move: Move the rover from one location to another.
2. CollectSample: Collect a sample at Location1.
3. TakePhoto: Take a photo at Location2.
4. AnalyzeRock: Analyze a rock at Location2.
5. AnalyzeSoil: Analyze soil at Location1.
6. TransmitData: Transmit the collected data after all other tasks are completed.

## Implementation
The implementation uses the AIMA planning and search libraries to define and solve the planning problem. The MarsRoverProblem class inherits from BasePlanningProblem and defines the initial state, goal state, and actions.

## Usage
To run the planning problem, execute the following code:
```python
from aimacode.search import astar_search
from mars_rover_problem import MarsRoverProblem

# Create an instance of the problem
mars_problem = MarsRoverProblem()

# Solve the problem using A* search with planning graph heuristic
solution = astar_search(mars_problem, mars_problem.h_pg_levelsum)

# Check if a solution is found
if solution:
    # Print the solution
    for action in solution.solution():
        print(action)
else:
    print("No solution found.")
```
## Sample Solution
```bash
Move(Base, Location2)
AnalyzeRock(Location2,)
TakePhoto(Location2,)
Move(Location2, Location1)
AnalyzeSoil(Location1,)
CollectSample(Location1,)
TransmitData()
```

