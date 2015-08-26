import numpy as np
from sklearn import svm
from sklearn.externals import joblib
from DataLoader import DataLoader
import ModelGlobals
import json
import os


class MachineLearningModel(object):


    def __init__(self):
        self.clf = svm.SVC(kernel='linear', C=1.0)
        self.X = [] # training data array
        self.y = [] # target data array

        with open(ModelGlobals.CHAMPION_MAP_INPUT_PATH, 'r') as fp:
            self.champ_map = json.load(fp)

        self.empty_array_width = 0
        for team in range(len(ModelGlobals.TEAMS)):
            for champion_possible in range(len(self.champ_map)):
                self.empty_array_width += 1


    def _findChampIndex(self, team, champ, offset):
        return self.champ_map[str(champ)] * ModelGlobals.TEAMS[team] + offset


    def _checkModelPath(self, serializePath, serializeFile, forceNew):
        if not os.path.isdir(serializePath):
            if os.path.exists(serializePath):
                raise IOError("{} already exists, not a directory".format(serializePath))
            else:
                os.mkdir(serializePath)

        full_pkl_path = serializePath + "/" + serializeFile

        if os.path.exists(full_pkl_path):
            if forceNew:
                os.remove(full_pkl_path)
            else:
                raise Exception("{} already exists".format(full_pkl_path))

        return full_pkl_path


    def loadData(self, stopCount=0):
        self.X = []
        self.y = []


        dl = DataLoader()
        matchGenerator = dl.getMatch()

        count = 0
        if stopCount != 0:
            print "Loading up to {} matches...".format(stopCount)
        else:
            print "Loading ALL matches..."

        try:
            while True:
                if stopCount > 0 and count == stopCount:
                    raise StopIteration
                current_list = []
                raw_data = matchGenerator.next()
                count += 1
                current_data = dl.filterMatchFields(raw_data)

                # data fields
                current_list.append(ModelGlobals.TIERS[current_data["matchTier"]])
                current_list.append(ModelGlobals.PATCHES[current_data["patch"]])

                offset = len(current_list)
                empty_fields = [0] * self.empty_array_width

                current_list.extend(empty_fields)

                for champion in current_data["teamA"]:
                    current_list[self._findChampIndex("teamA", champion, offset)] = 1
                for champion in current_data["teamB"]:
                    current_list[self._findChampIndex("teamB", champion, offset)] = 1

                self.X.append(current_list)

                # target value
                if current_data["winnerTeamA"]:
                    self.y.append(0)
                else:
                    self.y.append(1)


        except StopIteration as e:
            print "Done reading match data, {} matches".format(count)


    def testModel(self, size):
        if size <= 0:
            return
        score = 0
        for data in range(size):
            print "Prediction: {}, Expected: {}".format(self.clf.predict(self.X[-data])[0], self.y[-data])
            if self.clf.predict(self.X[-data])[0] == self.y[-data]:
                score += 1

        print "Tested with {} accuracy.".format(float(score)/float(size))


    def trainModel(self, sizeToLeave=0, testLeftover=False):
        if sizeToLeave == 0:
            self.clf.fit(self.X, self.y)
        elif sizeToLeave > 0:
            raise Exception("sizeToLeave should be less than or equal to 0")
        else:
            self.clf.fit(self.X[:sizeToLeave], self.y[:sizeToLeave])

        if testLeftover:
            self.testModel(-sizeToLeave)


    def serializeModel(self, serializePath, serializeFile, forceNew):
        full_pkl_path = self._checkModelPath(serializePath, serializeFile, forceNew)
        joblib.dump(self.clf, full_pkl_path)


    def loadModel(self, serializedPath, serializedFile):
        full_pkl_path = serializedPath + "/" + serializedFile
        self.clf = joblib.load(full_pkl_path)


    def predict(self, data):
        predict_X = []

        current_list.append(ModelGlobals.TIERS[data["matchTier"]])
        current_list.append(ModelGlobals.PATCHES[data["patch"]])

        offset = len(current_list)
        empty_fields = [0] * self.empty_array_width

        current_list.extend(empty_fields)

        for champion in data["teamA"]:
            current_list[self._findChampIndex("teamA", champion, offset)] = 1
        for champion in data["teamB"]:
            current_list[self._findChampIndex("teamB", champion, offset)] = 1

        predict_X.append(current_list)

        return self.clf.predict(X[-data])[0]
