from optparse import BadOptionError
import random
import numpy as np

visualizationStepTime=.05

class TSPSolver:
    def __init__(self):
        self.__options = [
            ('nn', self.nearestNeighbour),
            ('gc', self.greedyCycle),
            ('2r', lambda dmat, sol: self.kRegret(dmat, sol, 2)),
            ('3r', lambda dmat, sol: self.kRegret(dmat, sol, 3)),
            ('random', self.randomSolve)
        ]
        self.__vis=None
    
    def solve(self, tspInstance, algorithmName, visualize=False):
        dmatrix=tspInstance.dmatrix
        tspInstance.solution = self.genStartingNodes(dmatrix)
        algorithm = list(o[1] for o in self.__options if algorithmName == o[0])

        self.__vis = (lambda *, cycle=False: tspInstance.draw(cycle, visualizationStepTime)) if visualize else None
        if algorithm:
            algorithm[0](dmatrix, tspInstance.solution)
            if visualize :
                tspInstance.show()
        else:
            raise BadOptionError('No such algorithm')

    def genStartingNodes(self, dmatrix):
        c1 = random.randint(0, len(dmatrix)-1)
        c2 = np.argmax(dmatrix[c1])
        return [[c1], [c2]]

    def nearestNeighbour(self, dmatrix, solution):
        used=set()
        for n in solution[0]:
            used.add(n)
        for n in solution[1]:
            used.add(n)

        proxTable= tuple(sorted(range(len(dmatrix)), key=lambda node: dmatrix[i][node]) for i in range(len(dmatrix)))
        lastAddedNodes=[solution[0][-1], solution[1][-1]]
        while len(used)<len(dmatrix):
            if self.__vis: 
                self.__vis(cycle=False)

            if len(solution[0]) <= len(solution[1]):
                cycleNumber=0
                cycle = solution[0]
            else:
                cycleNumber=1
                cycle = solution[1]

            nodeToAdd=None
            for nodeToAdd in proxTable[lastAddedNodes[cycleNumber]]:
                if(nodeToAdd not in used):
                    used.add(nodeToAdd)
                    lastAddedNodes[cycleNumber]=nodeToAdd
                    break
                
            prevNodeIndex = len(cycle)-1
            bestDistance = -dmatrix[cycle[prevNodeIndex]][cycle[0]] + dmatrix[cycle[prevNodeIndex]][nodeToAdd] + dmatrix[cycle[0]][nodeToAdd]
            for i in range(len(cycle)):
                nexti=(i+1)%len(cycle)
                newDistance = -dmatrix[cycle[i]][cycle[nexti]] + dmatrix[cycle[i]][nodeToAdd] + dmatrix[cycle[nexti]][nodeToAdd]
                if(newDistance < bestDistance):
                    bestDistance=newDistance
                    prevNodeIndex=i
            cycle.insert(prevNodeIndex+1, nodeToAdd)

    def greedyCycle(self, dmatrix, solution):
        unused = [*range(0,len(dmatrix))]
        unused.remove(solution[0][0])
        unused.remove(solution[1][0])
        n = dmatrix[solution[0][0]].index(min(i for i in dmatrix[solution[0][0]] if i > 0))
        solution[0].append(n)
        unused.remove(n)
        n = dmatrix[solution[1][0]].index(min(i for i in dmatrix[solution[1][0]] if i > 0))
        solution[1].append(n)
        unused.remove(n)
        while len(unused) > 0:
            if self.__vis: 
                self.__vis(cycle=True)

            if len(solution[0]) <= len(solution[1]):
                cycleNumber=0
                cycle = solution[0]
            else:
                cycleNumber=1
                cycle = solution[1]

            bestNode = unused[0]
            bestInsert = 0
            n1 = cycle[0]
            n2 = cycle[1]
            bestCycleScore = -dmatrix[n1][n2] + dmatrix[bestNode][n1] + dmatrix[bestNode][n2]
            for node in unused:
                for insert, edge in enumerate((cycle[i], cycle[(i+1)%len(cycle)])for i in range(len(cycle))):
                    n1, n2 = edge
                    tempScore = -dmatrix[n1][n2] + dmatrix[node][n1] + dmatrix[node][n2]
                    if tempScore <= bestCycleScore:
                        bestNode = node
                        bestInsert = insert
                        bestCycleScore = tempScore
            unused.remove(bestNode)
            cycle.insert(bestInsert+1, bestNode)

    def kRegret(self, dmatrix, solution, k):
        used=set()
        for n in solution[0]:
            used.add(n)
        for n in solution[1]:
            used.add(n)

        while len(used)<len(dmatrix):
            if self.__vis: 
                self.__vis(cycle=True)

            if len(solution[0]) <= len(solution[1]):
                cycle = solution[0]
            else:
                cycle = solution[1]
            cycleEdges = list(enumerate((cycle[i], cycle[(i+1)%len(cycle)])for i in range(len(cycle))))

            candidates=[]
            for node in range(len(dmatrix)):
                if node not in used:
                    scores=[]
                    for i, edge in cycleEdges:
                        n1,n2=edge
                        tmp=(i+1, -dmatrix[n1][n2] + dmatrix[n1][node] + dmatrix[node][n2])
                        scores.append(tmp)
                    scores=sorted(scores, key=lambda e: e[1])
                    if len(scores) < 3:
                        tmp=(node, scores[0][0], scores[0][1])
                    else:
                        regret=0
                        for i in range(1,k):
                            if i >= len(scores):
                                break
                            regret+=scores[i][1]-scores[0][1]
                        tmp=(node, scores[0][0], (-regret)/max(0.000001,scores[0][1]))
                    candidates.append(tmp)
            candidates=sorted(candidates, key=lambda e: e[2])
            used.add(candidates[0][0])
            cycle.insert(candidates[0][1], candidates[0][0])

    def randomSolve(self, dmatrix, solution):
        tmp=list(range(len(dmatrix)))
        random.shuffle(tmp)
        solution[0]=tmp[:len(tmp)//2]
        solution[1]=tmp[len(tmp)//2:]

        
    def calcCycleScore(self, cycle, dmatrix):
        score=0
        for n1, n2 in ((cycle[i], cycle[(i+1)%len(cycle)])for i in range(len(cycle))):
            score+=dmatrix[n1][n2]
        return score
