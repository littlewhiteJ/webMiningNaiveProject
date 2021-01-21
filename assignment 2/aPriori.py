import json

class aPriori:
    def __init__(self, threshold=2):
        self.basketData = []
        self.freqDicts = []
        self.threshold = threshold

    def loadData(self, jsonFile):
        with open(jsonFile, 'r') as f:
            self.basketData = json.load(f)
    
    def runAPriori(self):
        while(1):
            newFreq = self.onePass()
            if newFreq == 0:
                break
    
    def returnFreqDicts(self):
        return self.freqDicts

    def onePass(self):
        if len(self.freqDicts) == 0:
            return self.firstPass()
        elif len(self.freqDicts) == 1:
            return self.secondPass()
        else:
            return self.morePass()
    
    def encodeKey(self, keyList):
        return json.dumps(keyList)

    def decodeKey(self, key):
        return json.loads(key)

    def generateSons(self, keyList):
        output = []
        for i in range(len(keyList)):
            kl = keyList.copy()
            kl.pop(i)
            output.append(kl)
        return output

    def firstPass(self):
        cntD_ = {}
        cntD = {}
        for basket in self.basketData:
            for item in basket:
                item = self.encodeKey([item])
                if item in cntD:
                    cntD[item] += 1
                else:
                    cntD[item] = 1
        # check frequent
        for key in cntD:
            if cntD[key] >= self.threshold:
                cntD_[key] = cntD[key]
        # save cntD to freqDicts
        if len(cntD_) != 0:
            self.freqDicts.append(cntD_)
        return len(cntD_)

    def secondPass(self):
        monoItems = list(self.freqDicts[0].keys())
        monoItems = [self.decodeKey(key)[0] for key in monoItems]
        # generate candidate keyList
        duoItems = [[monoItems[i], monoItems[j]] for i in range(len(monoItems) - 1) for j in range(i + 1, len(monoItems))]
        cntD = {self.encodeKey(keyList):0 for keyList in duoItems}
        cntD_ = {}
        for basket in self.basketData:
            for keyList in duoItems:
                if keyList[0] in basket and keyList[1] in basket:
                    cntD[self.encodeKey(keyList)] += 1
        # check frequent
        for key in cntD:
            if cntD[key] >= self.threshold:
                cntD_[key] = cntD[key]
        # save cntD to freqDicts
        if len(cntD_) != 0:
            self.freqDicts.append(cntD_)
        return len(cntD_)

    def morePass(self):
        monoItems = list(self.freqDicts[0].keys())
        monoItems = [self.decodeKey(key)[0] for key in monoItems]
        lastItems = list(self.freqDicts[-1].keys())
        lastItems = [self.decodeKey(key) for key in lastItems]
        # generate candidates
        thisItems = []
        for lastKeyList in lastItems:  
            for monoKey in monoItems:
                if monoKey not in lastKeyList:
                    lky = lastKeyList.copy()
                    lky.append(monoKey)
                    lky.sort()
                    if lky not in thisItems:
                        thisItems.append(lky)
        # prune candidates
        newItems = []
        # print(thisItems)
        for keyList in thisItems:
            thisSons = self.generateSons(keyList)
            fl = 1
            for son in thisSons:
                if son not in lastItems:
                    fl = 0
                    break
            if fl:
                newItems.append(keyList)
        # check baskets
        cntD = {self.encodeKey(keyList):0 for keyList in newItems}
        cntD_ = {}
        for basket in self.basketData:
            for keyList in newItems:
                fl = 1
                for key in keyList:
                    if key not in basket:
                        fl = 0
                        break
                if fl:
                    cntD[self.encodeKey(keyList)] += 1
        # check frequent
        for key in cntD:
            if cntD[key] >= self.threshold:
                cntD_[key] = cntD[key]
        # save cntD to freqDicts
        if len(cntD_) != 0:
            self.freqDicts.append(cntD_)
        return len(cntD_)

ap = aPriori()
ap.loadData('data.json')
ap.runAPriori()
print(ap.returnFreqDicts())