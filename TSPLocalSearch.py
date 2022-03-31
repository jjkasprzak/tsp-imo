
import random
from TSPSolver import visualizationStepTime
from optparse import BadOptionError
import time

class TSPLocalSearch:
    def __init__(self):
        self.__options = [
            ('steepest', self.steepestLocalSearch),
            ('greedy', self.greedyLocalSearch),
            ('random', self.randomSearch)
        ]
    
    def search(self, tspInstance, algorithmName, microSwaps, visualize=False,*, timeLimit=10):
        self.solution= tspInstance.solution
        self.dmatrix= tspInstance.dmatrix

        algorithm = list(o[1] for o in self.__options if algorithmName == o[0])
        
        self.__vis = (lambda: tspInstance.draw(True, visualizationStepTime)) if visualize else None
        self.macroMove = self.macroNodeSwap
        self.macroMoveGain = self.getMacroNodeSwapGain
        self.timeLimit = timeLimit
        if microSwaps == 'node':
            self.microMove = self.microNodeSwap
            self.microMoveGain = self.getMicroNodeSwapGain
        elif microSwaps == 'edge':
            self.microMove = self.microEdgeSwap
            self.microMoveGain = self.getMicroEdgeSwapGain
        else:
            raise BadOptionError('No such swap option')

        if algorithm:
            algorithm[0]()
            tspInstance.solution=self.solution
            if visualize:
                tspInstance.show()
        else:
            raise BadOptionError('No such algorithm')

    def getMacroNodeSwapGain(self, c1n, c2n):
        c1next = (c1n+1)%len(self.solution[0])
        c1prev = (c1n-1)%len(self.solution[0])
        c2next = (c2n+1)%len(self.solution[1])
        c2prev = (c2n-1)%len(self.solution[1])

        n1prev = self.solution[0][c1prev]
        n1 = self.solution[0][c1n]
        n1next = self.solution[0][c1next]

        n2prev = self.solution[1][c2prev]
        n2 = self.solution[1][c2n]
        n2next = self.solution[1][c2next]
        return -self.dmatrix[n1][n1prev]-self.dmatrix[n1][n1next]-self.dmatrix[n2][n2prev]-self.dmatrix[n2][n2next]+self.dmatrix[n1prev][n2]+self.dmatrix[n2][n1next]+self.dmatrix[n2prev][n1]+self.dmatrix[n2next][n1]

    def macroNodeSwap(self, c1n,c2n):
        tmp = self.solution[0][c1n]
        self.solution[0][c1n]=self.solution[1][c2n]
        self.solution[1][c2n]=tmp

    def getMicroNodeSwapGain(self, cycle, c1n, c2n):
        if c1n == c2n:
            return 0
        size=len(self.solution[cycle])
        c1next = (c1n+1)%size
        c1prev = (c1n-1)%size
        c2next = (c2n+1)%size
        c2prev = (c2n-1)%size

        n1prev = self.solution[cycle][c1prev]
        n1 = self.solution[cycle][c1n]
        n1next = self.solution[cycle][c1next]

        n2prev = self.solution[cycle][c2prev]
        n2 = self.solution[cycle][c2n]
        n2next = self.solution[cycle][c2next]
        return -self.dmatrix[n1][n1prev]-self.dmatrix[n1][n1next]-self.dmatrix[n2][n2prev]-self.dmatrix[n2][n2next]+self.dmatrix[n1prev][n2]+self.dmatrix[n2][n1next]+self.dmatrix[n2prev][n1]+self.dmatrix[n2next][n1]

    def microNodeSwap(self, cycle, n1, n2):
        tmp = self.solution[cycle][n1]
        self.solution[cycle][n1]=self.solution[cycle][n2]
        self.solution[cycle][n2]=tmp

    def getMicroEdgeSwapGain(self, cycle, c1n, c2n):
        if c1n == c2n:
            return 0
        size=len(self.solution[cycle])
        c1next = (c1n+1)%size
        c2next = (c2n+1)%size

        n1 = self.solution[cycle][c1n]
        n1next = self.solution[cycle][c1next]

        n2 = self.solution[cycle][c2n]
        n2next = self.solution[cycle][c2next]
        return -self.dmatrix[n1][n1next]-self.dmatrix[n2][n2next]+self.dmatrix[n1][n2]+self.dmatrix[n1next][n2next]

    def microEdgeSwap(self, cycle, n1, n2):
        if n2 < n1:
            tmp=n1
            n1=n2
            n2=tmp
        start = self.solution[cycle][:n1+1]
        rev = self.solution[cycle][n2:n1:-1]
        end = self.solution[cycle][n2+1:]
        self.solution[cycle]=start+rev+end

        

    def greedyLocalSearch(self):
        moves = []
        for i in range(len(self.solution[0])):
            for j in range(len(self.solution[1])):
                moves.append((i,j))
        for cycle in range(2):
            for i in range(len(self.solution[cycle])):
                for j in range(len(self.solution[cycle])):
                    moves.append((cycle,i,j))
        while True:
            random.shuffle(moves)
            noMove = True
            for move in moves:
                if len(move) == 2:#macro
                    if self.macroMoveGain(*move) < 0:
                        self.macroMove(*move)
                        noMove=False
                        break
                else:#micro
                    if self.microMoveGain(*move) < 0:
                        self.microMove(*move)
                        noMove=False
                        break
            if noMove:
                break
            if self.__vis: 
                self.__vis()

    def steepestLocalSearch(self):
        moves = []
        for i in range(len(self.solution[0])):
            for j in range(len(self.solution[1])):
                moves.append((i,j))
        for cycle in range(2):
            for i in range(len(self.solution[cycle])):
                for j in range(len(self.solution[cycle])):
                    moves.append((cycle,i,j))
        while True:
            bestGain=0
            bestMove=None
            for move in moves:
                gain=0
                if len(move) == 2:#macro
                    gain = self.macroMoveGain(*move)
                else:#micro
                    gain = self.microMoveGain(*move)
                if gain < bestGain:
                    bestGain = gain
                    bestMove = move

            if bestGain == 0:
                break
            else:
                if len(bestMove)==2:#macro
                    self.macroMove(*bestMove)
                else:#micro
                    self.microMove(*bestMove)
            if self.__vis: 
                self.__vis()

    def randomSearch(self):
        start = time.time()
        moves = []
        for i in range(len(self.solution[0])):
            for j in range(len(self.solution[1])):
                moves.append((i,j))
        for cycle in range(2):
            for i in range(len(self.solution[cycle])):
                for j in range(len(self.solution[cycle])):
                    moves.append((cycle,i,j))
        
        def cpSolution():
            return[self.solution[0][:],self.solution[1][:]]
        bestSolution = cpSolution()
        bestGain=0

        gainSum=0
        while self.timeLimit >= time.time()-start:
            move = moves[random.randint(0, len(moves)-1)]
            if len(move)==2:#macro
                gainSum += self.macroMoveGain(*move)
                self.macroMove(*move)
            else:#micro
                gainSum += self.microMoveGain(*move)
                self.microMove(*move)
            if gainSum < bestGain:
                bestGain = gainSum
                bestSolution=cpSolution()
            if self.__vis: 
                self.__vis()
        self.solution = bestSolution