from sklearn import datasets
from DataLoader import DataLoader
import json
import math
import os
import sys




def main():

    dl = DataLoader()
    matchGenerator = dl.getMatch()

    print json.dumps(dl.filterMatchFields(matchGenerator.next()), sort_keys=True, indent=4)
    print json.dumps(dl.filterMatchFields(matchGenerator.next()), sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
