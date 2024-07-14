from mars_rover_problem import MarsRoverProblem
from aimacode.search import astar_search

mars_problem = MarsRoverProblem()

solution = astar_search(mars_problem, mars_problem.h_pg_levelsum)

if solution:
    for action in solution.solution():
        print(action)
else:
    print("No solution found.")
