import random
from math import sqrt
import json

class kMeans:
    def __init__(self, nClusters):
        self.nClusters = nClusters
        self.dim = None

    def dis(self, p1, p2):
        squareSum = 0
        for i in range(len(p1)):
            squareSum += (p1[i] - p2[i]) ** 2
        return sqrt(squareSum)

    def initCenters(self, points):
        centers = []
        centers.append(points[random.randrange(len(points))])
        while(len(centers) != self.nClusters):
            minDis = []
            for p in points:
                pDis = []
                for c in centers:
                    pDis.append(self.dis(p, c))
                minDis.append(min(pDis))
            centers.append(points[minDis.index(max(minDis))])
        return centers

    def fit(self, points):
        self.dim = (len(points), len(points[0]))
        centers = self.initCenters(points)
        pointTags = []
        while(1):
            newPointTags = self.newCenters(centers, points)
            if newPointTags == pointTags:
                break
            else:
                pointTags = newPointTags
        return pointTags
        
    def newCenters(self, centers, points):
        pointTags = []
        zeroPoint = [0 for i in range(self.dim[1])]
        newClusterSum = [zeroPoint.copy() for i in range(self.nClusters)]
        newClusterNum = [0 for i in range(self.nClusters)]
        for p in points:
            pDis = []
            for c in centers:
                pDis.append(self.dis(p, c))
            pointTags.append(pDis.index(min(pDis)))
        for i in range(self.dim[0]):
            tag = pointTags[i]
            for d in range(self.dim[1]):
                newClusterSum[tag][d] += points[i][d]
                newClusterNum[tag] += 1
        newCenters = []
        for i in range(self.nClusters):
            c = []
            cSum = newClusterSum[i]
            for d in range(self.dim[1]):
                c.append(cSum[d])
            newCenters.append(c)
        return pointTags

        
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data



y = iris.target

km = kMeans(3)
print(X)
print(km.fit(X))

with open('x.json', 'w') as f:
    json.dump(X.tolist(), f)

with open('y.json', 'w') as f:
    json.dump(y.tolist(), f)