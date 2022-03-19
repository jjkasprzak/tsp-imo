import sys

import numpy as np
from TSPInstance import TSPInstance
from TSPSolver import TSPSolver


if __name__ == '__main__':
    instance = TSPInstance()
    solver = TSPSolver()
    for filename in ['kroA100.tsp', 'kroB100.tsp']:
        instance.loadInstance('instances/'+filename)
        for algorithm in ['nn', 'gc', '2r', '3r']:
            print(filename + ' ' + algorithm)
            scores=[]
            for i in range(1):
                solver.solve(instance, algorithm)
                scores.append(instance.score())
            print(str(sum(scores)//len(scores)) + ' (' + str(min(scores)) + ' - ' + str(max(scores)) + ')')
            instance.show()