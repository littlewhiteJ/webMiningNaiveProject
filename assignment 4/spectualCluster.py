import json
import numpy as np


class SpectualCluster:
    def __init__(self):
        self.adjacencyMatrix = None
        self.nodeAmount = 0
    
    def loadAdjacencyMatrix(self, adjMatrixPath):
        with open(adjMatrixPath, 'r') as f:
            aM = json.load(f)
        self.adjacencyMatrix = np.array(aM)
        self.nodeAmount = self.adjacencyMatrix.shape[0]
    
    def laplace(self):
        A = self.adjacencyMatrix
        D = np.zeros(self.adjacencyMatrix.shape)
        for i in range(self.nodeAmount):
            D[i, i] = np.sum(A[i])
        return D - A

    def cluster(self):
        L = self.laplace()
        eigenValue, eigenVector = np.linalg.eigh(L)
        eigenVector = eigenVector.T
        eigens = [[eigenValue[i], eigenVector[i]] for i in range(len(eigenValue))]
        eigens.sort(key=lambda x:x[0])
        theVector = eigens[1][1]
        return theVector

sc = SpectualCluster()
sc.loadAdjacencyMatrix('matrix.json')
print(sc.cluster())

