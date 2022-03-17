import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys

def loadTSPCoords(path):
    coords=[]
    header = True

    f=open(path, 'r')
    for line in f.readlines():
        if not header:
            if 'EOF' in line:
                break
            else:
                nodeIndex, x, y = (int(word) for word in line.split())
                coords.append(np.array([x,y]))
        elif 'NODE_COORD_SECTION' in line:
            header = False
    f.close()
    return coords

def calcDistanceMatrix(coords):
    dmatrix=[]
    for c1 in coords:
        c1distances=[]
        for c2 in coords:
            c1distances.append(int(np.linalg.norm(c1-c2)+.5))
        dmatrix.append(c1distances)
    return dmatrix

def genStartingNodes(dmatrix):
    c1 = random.randint(0, len(dmatrix)-1)
    c2 = np.argmax(dmatrix[c1])
    return (c1,c2)

def nearestNeighbour(dmatrix, start):
    solution=[[start[0]], [start[1]]]
    used=set()
    used.add(start[0])
    used.add(start[1])

    proxTable= tuple(sorted(range(len(dmatrix)), key=lambda node: dmatrix[i][node]) for i in range(len(dmatrix)))

    while len(used)<len(dmatrix):
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
        
    return solution

        
def greedyCycle(dmatrix, start):
    pass
def twoRegret(dmatrix, start):
    pass
def threeRegret(dmatrix, start):
    pass

if __name__ == '__main__':
    coords = loadTSPCoords('instances/kroA100.tsp')
    dmatrix = calcDistanceMatrix(coords)
    c1,c2 = nearestNeighbour(dmatrix, genStartingNodes(dmatrix))

    g1 = nx.Graph()
    g2 = nx.Graph()
    g1.add_edges_from((c1[i], c1[(i+1)%len(c1)])for i in range(len(c1)))
    g2.add_edges_from((c2[i], c2[(i+1)%len(c2)])for i in range(len(c2)))
    coordDict=dict(enumerate(coords))
    nx.draw(g1, coordDict, node_color="#FF0000", edge_color="#FF0000", node_size=40)
    nx.draw(g2, coordDict, node_color="#0000FF", edge_color="#0000FF", node_size=40)
    plt.show()