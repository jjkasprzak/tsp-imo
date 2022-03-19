import sys

from TSPInstance import TSPInstance
from TSPSolver import TSPSolver

if __name__ == '__main__':
    instance = TSPInstance()
    instance.loadInstance('instances/kroA100.tsp')
    solver = TSPSolver()
    solver.solve(instance, 'nn', visualize=True)
    print(instance.solution)
    print(instance.score())