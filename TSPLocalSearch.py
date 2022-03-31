


class TSPLocalSearch:
    def __init__(self):
        self.__options = [
            ('steepest', self.steepestLocalSearch),
            ('greedy', self.greedyLocalSearch),
            ('random', self.randomSearch)
        ]
    
    def search(self, tspInstance):
        self.solution= tspInstance.solution
        self.dmatrix= tspInstance.dmatrix

        tmp = tspInstance.score()
        gain = self.getMacroNodeSwapGain(20, 40)
        self.macroNodeSwap(20, 40)
        print(gain == tspInstance.score()-tmp)

        tmp = tspInstance.score()
        gain = self.getMicroNodeSwapGain(0,20, 40)
        self.microNodeSwap(0, 20, 40)
        print(gain == tspInstance.score()-tmp)

        tmp = tspInstance.score()
        gain = self.getMicroEdgeSwapGain(0,20, 40)
        self.microEdgeSwap(0, 20, 40)
        print(gain == tspInstance.score()-tmp)

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

        

    def greedyLocalSearch(self, tspInstance):
        pass

    def steepestLocalSearch(self, tspInstance):
        pass

    def randomSearch(self, tspInstance):
        pass