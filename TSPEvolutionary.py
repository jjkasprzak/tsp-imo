from TSPLocalSearch import *
from TSPSolver import *
import random

def steadyState(tspInstance, populationSize=20, *, timeLimit=200, localSearch=True, visualize=False):
    start = time.time()
    vis = (lambda *, cycle=False: tspInstance.draw(cycle, visualizationStepTime))
    solver = TSPSolver()
    search = TSPLocalSearch()
    
    #generowanie populacji
    population=[]
    for i in range(populationSize):
        search.search(tspInstance, 'steepestWithCandidates', 'edge', lambda inst: solver.solve(inst, 'random'))
        score=tspInstance.score()
        population.append((score, tspInstance.solution))
    
    while timeLimit >= time.time()-start:
        random.shuffle(population)

        #rekombinacja
        s1,s2=population[0][1], population[1][1]
        tspInstance.solution=s1
        e1=tspInstance.getSolutionEdges()
        tspInstance.solution=s2
        e2=tspInstance.getSolutionEdges()
        edges=set()
        for ei in [*e1[0], *e1[1]]:
            for ej in [*e2[0], *e2[1]]:
                if ei == ej or ei == tuple(reversed(ej)):
                    edges.add(ei)
        
        newSolution=[]
        for c in s1:
            lastNode = c[-1]
            resultingC=[]
            addLast=False
            for node in c:
                if (lastNode, node) in edges or (node, lastNode) in edges:
                    if len(resultingC) == 0:
                        addLast=True
                    elif resultingC[-1] != lastNode:
                        resultingC.append(lastNode)
                    resultingC.append(node)
                lastNode=node
            if addLast == True and resultingC[-1] != c[-1]:
                resultingC.append(c[-1])
            if len(resultingC) == 0:
                resultingC.append(c[0])
            newSolution.append(resultingC)
        tspInstance.solution=newSolution
        solver.kRegret(tspInstance.dmatrix, tspInstance.solution, 2)
        if localSearch:
            search.search(tspInstance, 'steepestWithCandidates', 'edge', lambda inst: None)
        score = tspInstance.score()
        maxIndex=None
        maxScore=0
        for i in range(populationSize):
            if population[i][0] == score:
                maxIndex=None
                break
            if population[i][0]>maxScore:
                maxIndex=i
                maxScore=population[i][0]
        if maxIndex is not None:
            population[maxIndex]=(score, tspInstance.solution)
        tspInstance.solution = min(population, key= lambda e: e[0])[1]
        if visualize:
            vis()
    tspInstance.solution = min(population, key= lambda e: e[0])[1]







    

