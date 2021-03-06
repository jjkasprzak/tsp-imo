
import random

import numpy as np
from TSPSolver import visualizationStepTime, TSPSolver
from optparse import BadOptionError
import time

class TSPLocalSearch:
    def __init__(self):
        self.__options = [
            ('steepestWithCandidates', self.steepestLocalSearchWithCandidates),
            ('steepestWithList', self.steepestLocalSearchWithList),
            ('steepest', self.steepestLocalSearch),
            ('greedy', self.greedyLocalSearch),
            ('random', self.randomSearch)
        ]
        self.__extensionOptions = [
            ('msls', self.msls),
            ('ils1', self.ils1),
            ('ils2', self.ils2)
        ]
    
    def search(self, tspInstance, algorithmName, microSwaps, solve, visualize=False,*, timeLimit=10, extensionName=None):
        def newsol():
            solve(tspInstance)
            self.solution= tspInstance.solution
        self.genNewSolution=newsol
        self.score = lambda: tspInstance.score()
        self.tspInstance=tspInstance

        self.genNewSolution()
        self.dmatrix= tspInstance.dmatrix

        algorithm = list(o[1] for o in self.__options if algorithmName == o[0])
        extension = list(o[1] for o in self.__extensionOptions if extensionName == o[0])
        
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
            if extensionName:
                if extension:
                    extension[0](algorithm[0])
                else:
                    raise BadOptionError('No such extension')
            else:
                algorithm[0]()

            if visualize:
                tspInstance.show()
        else:
            raise BadOptionError('No such algorithm')
        tspInstance.solution = self.solution

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
        bonus = 0
        if c1next == c2n or c2next == c1n:
            bonus=2*self.dmatrix[n1][n2]
        return bonus-self.dmatrix[n1][n1prev]-self.dmatrix[n1][n1next]-self.dmatrix[n2][n2prev]-self.dmatrix[n2][n2next]+self.dmatrix[n1prev][n2]+self.dmatrix[n2][n1next]+self.dmatrix[n2prev][n1]+self.dmatrix[n2next][n1]

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

    def steepestLocalSearchWithList(self):
        def transformMove(move):
            res=None
            if len(move)==2:#macro
                res = (self.solution[0].index(move[0]),self.solution[1].index(move[1]))
            else:#micro
                res = (move[0], self.solution[move[0]].index(move[1]),self.solution[move[0]].index(move[2]))
            return res
        moves = []
        mset=set()
        for ip, i in enumerate(self.solution[0]):
            for jp, j in enumerate(self.solution[1]):
                moves.append(((i,j), self.macroMoveGain(ip,jp)))
                mset.add((i,j))
        for cycle in range(2):
            for ip, i in enumerate(self.solution[cycle]):
                for jp, j in enumerate(self.solution[cycle]):
                    moves.append(((cycle,i,j), self.microMoveGain(cycle,ip,jp)))
                    mset.add((cycle,i,j))
        ml=sorted(moves, key=lambda e: e[-1])
        while True:
            move=[]
            moves=[]
            for ip, i in enumerate(self.solution[0]):
                for jp, j in enumerate(self.solution[1]):
                    if (i,j) not in mset:
                        mset.add((i,j))
                        moves.append(((i,j), self.macroMoveGain(ip,jp)))
                    
            for cycle in range(2):
                for ip, i in enumerate(self.solution[cycle]):
                    for jp, j in enumerate(self.solution[cycle]):
                        if (cycle,i,j) not in mset:
                            moves.append(((cycle,i,j), self.microMoveGain(cycle,ip,jp)))
                            mset.add((cycle,i,j))
            ml=sorted(moves+ml, key=lambda e: e[-1])
            
            best=0
            for pos in range(len(ml)):
                mset.remove(ml[pos][0])
                try:
                    tmp = transformMove(ml[pos][0])
                    if len(tmp)==2:#macro
                        gain = self.macroMoveGain(*tmp)
                    else:
                        gain = self.microMoveGain(*tmp)
                    if gain < 0:
                        if gain < best:
                            move=tmp
                            best=gain
                    if best != 0 and pos+1<len(ml) and best < ml[pos+1][-1]:
                        break
                except ValueError:
                    pass
            if best==0:
                break
            if len(move)==2:#macro
                self.macroMove(*move)
            else:#micro
                self.microMove(*move)
            ml=ml[pos+1:]
            if self.__vis: 
                self.__vis()

    def steepestLocalSearchWithCandidates(self):
        indexes=dict()
        def bestMicro(c, n1,n2):
            i1,i2=[indexes[n1], indexes[n2]]
            m1=(c, i1, i2)
            m2=(c, (i1-1)%len(self.solution[c]), (i2-1)%len(self.solution[c]))
            g1=self.microMoveGain(*m1)
            g2=self.microMoveGain(*m2)
            if g1< g2:
                return m1,g1
            return m2,g2
        def bestMacro(n1,n2):
            i1,i2=[indexes[n1], indexes[n2]]
            m1=((i1+1)%len(self.solution[0]), i2)
            m2=((i1-1)%len(self.solution[0]), i2)
            #m3=(i1, (i2+1)%len(self.solution[1]))
            #m4=(i1, (i2-1)%len(self.solution[1]))
            ms=[m1,m2]#,m3,m4]
            gs=list(self.macroMoveGain(*m) for m in ms)
            best=np.argmax(gs)
            return ms[best], gs[best]

        nodes=range(len(self.dmatrix))
        proxTable= tuple(sorted(range(len(self.dmatrix)), key=lambda node: self.dmatrix[i][node]) for i in range(len(self.dmatrix)))
        moves=[]
        for n1 in nodes:
            for n2 in proxTable[n1][1:10]:
                moves.append((n1,n2))
        s0=set(self.solution[0])
        while True:
            ind=0
            for node in self.solution[0]:
                indexes[node]=ind
                ind+=1
            ind=0
            for node in self.solution[1]:
                indexes[node]=ind
                ind+=1
            
            bestGain=0
            bestMove=None
            for n1,n2 in moves:
                if n1 in s0:
                    if n2 in s0:#micro
                        move,gain=bestMicro(0,n1,n2)
                    else:#macro
                        move,gain=bestMacro(n1,n2)
                else:
                    if n2 in s0:#macro
                        move,gain=bestMacro(n2,n1)
                    else:#micro
                        move,gain=bestMicro(1,n1,n2)
                if gain < bestGain:
                    bestGain = gain
                    bestMove = move
            if bestGain == 0:
                break
            else:
                if len(bestMove)==2:#macro
                    s0.remove(self.solution[0][bestMove[0]])
                    s0.add(self.solution[1][bestMove[1]])
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
        
        bestSolution = [self.solution[0][:],self.solution[1][:]]
        bestGain=0

        gainSum=0
        while self.timeLimit >= time.time()-start:
            move = moves[random.randint(0, len(moves)-1)]
            if len(move)==2:#macro
                gainSum = gainSum + self.macroMoveGain(*move)
                self.macroMove(*move)
            else:#micro
                gainSum = gainSum + self.microMoveGain(*move)
                self.microMove(*move)
            if gainSum < bestGain:
                bestGain = gainSum
                bestSolution=[self.solution[0][:],self.solution[1][:]]
            if self.__vis: 
                self.__vis()
        self.solution[0]=bestSolution[0]
        self.solution[1]=bestSolution[1]

    def msls(self, ls):
        ls()
        bestScore=self.score()
        bestSolution=self.solution

        for i in range(100):
            self.genNewSolution()
            ls()
            score = self.score()
            if score < bestScore:
                bestScore=score
                bestSolution=self.solution

            if self.__vis: 
                self.__vis()
        self.solution=bestSolution

    def ils1(self, ls):
        start = time.time()
        moves = []
        for i in range(len(self.solution[0])):
            for j in range(len(self.solution[1])):
                moves.append((i,j))
        for cycle in range(2):
            for i in range(len(self.solution[cycle])):
                for j in range(len(self.solution[cycle])):
                    moves.append((cycle,i,j))


        ls()
        bestScore=self.score()
        bestSolution=self.solution

        while self.timeLimit >= time.time()-start:
            self.solution=[bestSolution[0][:], bestSolution[1][:]]
            self.tspInstance.solution=self.solution
            for i in range(int(len(self.dmatrix)*0.08)):
                move = moves[random.randint(0, len(moves)-1)]
                if len(move)==2:#macro
                    self.macroMove(*move)
                else:#micro
                    self.microMove(*move)
            ls()
            score = self.score()
            if score < bestScore:
                bestScore=score
                bestSolution=self.solution

            if self.__vis: 
                self.__vis()
        self.solution=bestSolution
    def ils2(self, ls):
        start = time.time()
        ls()
        bestScore=self.score()
        bestSolution=self.solution
        solver = TSPSolver()

        while self.timeLimit >= time.time()-start:
            self.solution=[bestSolution[0][:], bestSolution[1][:]]
            self.tspInstance.solution=self.solution
            tmp = list(range(len(self.dmatrix)))
            random.shuffle(tmp)
            toRemove = tmp[0:int(len(self.dmatrix)*0.2)]
            
            s0=set(self.solution[0])
            for node in toRemove:
                if node in s0:
                    self.solution[0].remove(node)
                else:
                    self.solution[1].remove(node)
            solver.kRegret(self.dmatrix, self.solution, 2)
            score = self.score()
            if score < bestScore:
                bestScore=score
                bestSolution=self.solution

            if self.__vis: 
                self.__vis()
        self.solution=bestSolution