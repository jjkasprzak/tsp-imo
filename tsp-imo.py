import numpy as np

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
print(calcDistanceMatrix(loadTSPCoords("kroA100.tsp")))