import numpy as np
import json

class PageRank:
    def __init__(self, nPages, beta, dataPath):
        self.nPages = nPages
        self.beta = beta
        self.dataPath = dataPath
        self.adjacencyMatrix = None
    
    def generateMatrix(self):
        randomBase = np.random.rand(self.nPages, self.nPages)
        lineSum = np.sum(randomBase, axis=0)
        self.adjacencyMatrix = randomBase / lineSum
        jsonMatrix = self.adjacencyMatrix.tolist()
        with open(self.dataPath, 'w') as f:
            json.dump(jsonMatrix, f)

    def setMatrix(self, adjacencyMatrix):
        self.adjacencyMatrix = adjacencyMatrix

    def run(self, epsilon):

        v = (np.ones(self.nPages) / self.nPages).T
        e = (np.ones(self.nPages) / self.nPages).T
        while(1):
            v_ = self.beta * self.adjacencyMatrix.dot(v) + (1 - self.beta) * e / self.nPages
            diffV = np.sum(np.abs(v - v_))
            if diffV > epsilon:
                v = v_
            else:
                vSum = np.sum(v_)
                return v_ / vSum

# set the matrix by user
'''
pr = PageRank(3, 0.8, 'matrix.json')
m = np.array([[0.5, 0.5, 0], [0.5, 0, 0], [0, 0.5, 1]])
pr.setMatrix(m)
print(pr.run(0.0000000001))
'''

# set the matrix by random, the data is set in 'matrix.json'
pr = PageRank(20, 0.8, 'matrix.json')
pr.generateMatrix()
print(pr.run(0.0000000001))
