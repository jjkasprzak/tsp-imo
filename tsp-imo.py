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
            bestSolution=None
            bestScore=None
            for i in range(1000):
                solver.solve(instance, algorithm, visualize=False)
                scores.append(instance.score())
                if bestScore == None or scores[-1] < bestScore:
                    bestScore=scores[-1]
                    bestSolution=instance.solution
            
            print(str(sum(scores)//len(scores)) + ' (' + str(min(scores)) + ' - ' + str(max(scores)) + ')')
            if bestScore:
                print(bestScore)
                instance.solution=bestSolution
                instance.show()