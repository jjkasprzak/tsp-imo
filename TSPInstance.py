import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class TSPInstance:
    def __init__(self):
        self.coords=None
        self.dmatrix=None
        self.solution=None

    def __getSolutionEdges(self):
        c1,c2 = self.solution
        return [list((c1[i], c1[(i+1)%len(c1)])for i in range(len(c1))), list((c2[i], c2[(i+1)%len(c2)])for i in range(len(c2)))]

    def score(self):
        if self.solution:
            res=0
            c1,c2 = self.__getSolutionEdges()
            for n1,n2 in c1:
                res+=self.dmatrix[n1][n2]
            for n1,n2 in c2:
                res+=self.dmatrix[n1][n2]
            return res
        return None


    def loadInstance(self, path):
        self.__loadTSPCoords(path)
        self.__calcDistanceMatrix()
        self.solution=None

    def draw(self, cycle=True):
        g = nx.Graph()
        g.add_nodes_from(i for i in range(len(self.coords)))
        
        if self.solution:
            c1,c2= self.__getSolutionEdges()
            if not cycle:
                c1=c1[:-1]
                c2=c2[:-1]
            g1 = nx.Graph()
            g2 = nx.Graph()
            g1.add_edges_from(c1)
            g2.add_edges_from(c2)
            coordDict=dict(enumerate(self.coords))

        plt.clf()
        nx.draw(g, coordDict, node_color="#000000", edge_color="#000000", node_size=40)
        if self.solution:
            nx.draw(g1, coordDict, node_color="#FF0000", edge_color="#FF0000", node_size=40)
            nx.draw(g2, coordDict, node_color="#0000FF", edge_color="#0000FF", node_size=40)
        plt.draw()
        plt.pause(0.5)

    def show(self):
        self.draw()
        plt.show()

    def __loadTSPCoords(self, path):
        self.coords=[]
        header = True

        f=open(path, 'r')
        for line in f.readlines():
            if not header:
                if 'EOF' in line:
                    break
                else:
                    nodeIndex, x, y = (int(word) for word in line.split())
                    self.coords.append(np.array([x,y]))
            elif 'NODE_COORD_SECTION' in line:
                header = False
        f.close()
    
    def __calcDistanceMatrix(self):
        self.dmatrix=[]
        for c1 in self.coords:
            c1distances=[]
            for c2 in self.coords:
                c1distances.append(int(np.linalg.norm(c1-c2)+.5))
            self.dmatrix.append(c1distances)
