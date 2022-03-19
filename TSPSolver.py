from optparse import BadOptionError
import random
import numpy as np

class TSPSolver:
    def __init__(self):
        self.__options = [
            ('nn', self.nearestNeighbour),
            ('gc', self.greedyCycle),
            ('2r', self.twoRegret),
            ('3r', self.threeRegret)
        ]
    
    def solve(self, tspInstance, algorithmName, visualize=False):
        dmatrix=tspInstance.dmatrix
        tspInstance.solution = self.genStartingNodes(dmatrix)
        algorithm = list(o[1] for o in self.__options if algorithmName == o[0])

        self.__vis = tspInstance.draw if visualize else None
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
        used.add(solution[0][0])
        used.add(solution[1][0])

        proxTable= tuple(sorted(range(len(dmatrix)), key=lambda node: dmatrix[i][node]) for i in range(len(dmatrix)))

        while len(used)<len(dmatrix):
            if self.__vis: 
                self.__vis()

            cycle = solution[0] if len(solution[0]) <= len(solution[1]) else solution[1]

            nodeToAdd=None
            for nodeToAdd in proxTable[cycle[-1]]:
                if(nodeToAdd not in used):
                    used.add(nodeToAdd)
                    break
            prevNodeIndex = len(cycle)-1
            bestDistance = dmatrix[cycle[prevNodeIndex]][nodeToAdd]
            for i in range(len(cycle)):
                newDistance=dmatrix[cycle[i]][nodeToAdd]
                if(newDistance < bestDistance):
                    bestDistance=newDistance
                    prevNodeIndex=i
            cycle.insert(prevNodeIndex+1, nodeToAdd)


    def greedyCycle(self, dmatrix, start):
        pass
    def twoRegret(self, dmatrix, start):
        pass
    def threeRegret(self, dmatrix, start):
        pass
