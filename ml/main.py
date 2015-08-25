import numpy as np
from sklearn import svm
from DataLoader import DataLoader
import json
import math
import os
import sys


TIERS = {
    "NO_RANK":0,
    "BRONZE":0.2,
    "SILVER":0.4,
    "GOLD":0.6,
    "PLATINUM":0.8,
    "DIAMOND+":1
}


PATCHES = {
    "5.11":0,
    "5.14":1
}


def main():

    dl = DataLoader()
    matchGenerator = dl.getMatch()

    X = []
    y = []

    count = 0
    try:
        while True:
            current_list = []
            raw_data = matchGenerator.next()
            current_data = dl.filterMatchFields(raw_data)

            # data fields
            current_list.append(TIERS[current_data["matchTier"]])
            current_list.append(PATCHES[current_data["patch"]])
            X.append(current_list)

            # target value
            if current_data["winnerTeamA"]:
                y.append(0)
            else:
                y.append(1)

            # print json.dumps(dl.filterMatchFields(raw_data), sort_keys=True, indent=4)
            if count > 100:
                raise StopIteration
            count += 1

    except StopIteration as e:
        print "Done reading match data."

    print X
    print y
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X[:-1], y[:-1])

    print clf.predict(X[-1])

    print y[-1]


if __name__ == "__main__":
    main()
