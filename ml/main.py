import numpy as np
from sklearn import svm
from DataLoader import DataLoader
import json
import math
import os
import sys

CHAMPION_MAP_INPUT_PATH = "championMap.json"

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


def findChampIndex(champ_map, team, champ):
    return champ_map[str(champ)] * (team + 1) + 2 # 2 for matchTier and patch fields


def main():

    with open(CHAMPION_MAP_INPUT_PATH, 'r') as fp:
        champ_map = json.load(fp)

    dl = DataLoader()
    matchGenerator = dl.getMatch()

    X = []
    y = []

    arrayWidth = 0
    for team in range(2):
        for champion_possible in range(len(champ_map)):
            arrayWidth += 1

    count = 0
    try:
        while True:
            count += 1
            current_list = []
            raw_data = matchGenerator.next()
            current_data = dl.filterMatchFields(raw_data)

            # data fields
            current_list.append(TIERS[current_data["matchTier"]])
            current_list.append(PATCHES[current_data["patch"]])

            empty_fields = [0] * arrayWidth

            current_list.extend(empty_fields)

            for champion in current_data["teamA"]:
                current_list[findChampIndex(champ_map, 0, champion)] = 1
            for champion in current_data["teamB"]:
                current_list[findChampIndex(champ_map, 1, champion)] = 1

            X.append(current_list)

            # target value
            if current_data["winnerTeamA"]:
                y.append(0)
            else:
                y.append(1)


    except StopIteration as e:
        print "Done reading match data."

    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X[:-1], y[:-1])

    print clf.predict(X[-1])

    print y[-1]


if __name__ == "__main__":
    main()
