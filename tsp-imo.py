import sys

from TSPInstance import TSPInstance
from TSPSolver import TSPSolver


if __name__ == '__main__':
    instance = TSPInstance()
    solver = TSPSolver()
    for filename in ['kroA100.tsp', 'kroB100.tsp']:
        instance.loadInstance('instances/'+filename)
        
        #SIMPLE HEURISTIC TESTING
        #for algorithm in ['nn', 'gc', '2r', '3r']:
        #    print(filename + ' ' + algorithm)
        #    scores=[]
        #    bestSolution=None
        #    bestScore=None
        #    for i in range(1):
        #        solver.solve(instance, algorithm, visualize=True)
        #        scores.append(instance.score())
        #        if bestScore == None or scores[-1] < bestScore:
        #            bestScore=scores[-1]
        #            bestSolution=instance.solution
        #    
        #    print(str(sum(scores)//len(scores)) + ' (' + str(min(scores)) + ' - ' + str(max(scores)) + ')')
        #    if bestScore:
        #        print(bestScore)
        #        instance.solution=bestSolution
        #        instance.show()