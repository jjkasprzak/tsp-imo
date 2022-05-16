import sys
import time

from TSPInstance import TSPInstance
from TSPSolver import TSPSolver
from TSPLocalSearch import TSPLocalSearch


if __name__ == '__main__':
    instance = TSPInstance()
    solver = TSPSolver()
    lsearch= TSPLocalSearch()
    for filename in ['kroA200.tsp', 'kroB200.tsp']:
        instance.loadInstance('instances/'+filename)
        for heuristics in ['random']:
            for microSwap in ['edge']:#['node', 'edge']:
                for algorithm in ['steepestWithList']:#['random', 'greedy', 'steepest', 'steepestWithList']:
                    for extension in ['msls', 'ils1', 'ils2']:
                        note = filename + '_' + heuristics + '-' + algorithm + '_search_with_' + microSwap + '_swap_and_' + extension
                        print(note)
                        scores=[]
                        times=[]
                        bestScore=None
                        bestSolution=None
                        for i in range(10):
                            start=time.time()
                            solve = lambda inst: solver.solve(inst, heuristics, False)
                            lsearch.search(instance, algorithm, microSwap, solve, False, timeLimit=750, extensionName=extension)
                            times.append(time.time()-start)
                            scores.append(instance.score())
                            if bestScore == None or scores[-1] < bestScore:
                                bestScore=scores[-1]
                                bestSolution=instance.solution            
                        print('score: ' + str(sum(scores)//len(scores)) + ' (' + str(min(scores)) + ' - ' + str(max(scores)) + ')')
                        print('time: ' + str(round(sum(times)/len(times),2)) + ' (' + str(round(min(times),2)) + ' - ' + str(round(max(times),2)) + ')')
                        if bestScore:
                            instance.solution=bestSolution
                            instance.saveImg('images/' + note+'.png')    


        
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