'''


Finally, we generate .json data files for each individual champion with fields separated by region, patch queueType, tier, etc.

We will find all existing champions by id and insert them into the CHAMPION_DATA dictionary.
We will then scan through all match files and sum up all data for a particular champion by
inserting it into the dictionary. When we reach the end of each rank we will dump the data
into an output file which we will call a "midpoint file" e.g. {oriannaId}-na-511-ranked-bronze.json

At the very end of this script we will search through all these midpoint files and paste them
together into a single output file. This way we can clean out our dictionary structure in every rank instead
of dumping it all at the very end (which would potentially consume a lot of memory).


Sample json champion output data:

{
  "Orianna": {
    "NA": {
      "5.11": {
        "NORMAL_5X5": {
          "NO_RANK": {}
        },
        "RANKED_SOLO": {
          "BRONZE": {
            "winRate": 60,
            "matchesCounted": 100,
            "averageCsPerMin": 10,
            "averageGoldPerMin": 200,
            "averageKda": 6,
            "averageDamageDealt": 14000,
            "mostCommonItems": {
              "item0": {
                "itemId": 123,
                "isApItem": "yes",
                "buyPercentage": 80,
                "averageTimeBought": "15:00"
              },
              "item1": {
                "itemId": 456,
                "isApItem": "no",
                "buyPercentage": 65,
                "averageTimeBought": "25:00"
              }
            }
          },
          "SILVER": {},
          "GOLD": {},
          "PLATINUM": {},
          "DIAMOND": {},
          "MASTER": {},
          "CHALLENGER": {}
        }
      },
      "5.14": {
        "NORMAL_5X5": {},
        "RANKED_SOLO": {
          "BRONZE": {},
          "SILVER": {},
          "GOLD": {},
          "PLATINUM": {},
          "DIAMOND": {},
          "MASTER": {},
          "CHALLENGER": {}
        }
      }
    }
  }
}


'''


from RiotAPI import RiotAPI, Request
import apiKey
import json
import math
import os
import sys

API_KEY = apiKey.API_KEY

NORMAL_INPUT_PATH_BASE = "MATCH_DATA/{patch}/NORMAL_5X5/{region}/{filepatch}-normal-{fileregion}-{fileindex}.json"
RANKED_INPUT_PATH_BASE = "MATCH_DATA/{patch}/RANKED_SOLO/{region}/{tier}/{filepatch}-ranked-{fileregion}-{filetier}-{fileindex}.json"
MIDPOINT_FILE_BASE = "data/champion/{championId}-{region}-{patch}-{queueType}-{rank}.json"
OUTPUT_PATH_BASE = "data/champion/{championName}.json"

STATIC_DATA_CHAMPIONS = "data/static/champions.json"
STATIC_DATA_ITEMS = {
    "5.11":"data/static/items511.json",
    "5.14":"data/static/items514.json"
}

CHAMPION_DATA = {}

'''
    I need to consider if we will have "hidden" fields that won't make it into the final output, for example it might be slightly
    more accurate to keep track of matches won and continuously recalculate winRate, or continuously recalculate winRate via previous winRate and matchesCounter

    however the change in accuracy is probably negligible and having edge cases like that isn't ideal
'''
CHAMPION_DATA_FIELDS = [
    "winRate",
    "matchesCounted",
    "averageCsPerMin",
    "averageGoldPerMin",
    "averageKda",
    "averageDamageDealt",
    "mostCommonItems"
]

REGIONS = ["NA"] #["BR", "EUNE", "EUW", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]
PATCHES = ["5.11", "5.14"]
QUEUETYPES = {
    "NORMAL_5X5":"normal",
    "RANKED_SOLO":"ranked"
    }
RANKED_TIERS = {
    "NORMAL_5X5":{
        "NO_RANK"
    },
    "RANKED_SOLO":{
        "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "CHALLENGER"
    }
}


def constructChampionDict():
    global CHAMPION_DATA = {}
    with open(STATIC_DATA_CHAMPIONS, 'r') as fp:
        static_champion_data = json.load(fp)

        for champion in static_champion_data["data"]:
            CHAMPION_DATA[champion["id"]] = {}
            CHAMPION_DATA[champion["id"]]["matchesCounted"] = 0
            CHAMPION_DATA[champion["id"]]["mostCommonItems"] = {}


def flushAllData(region, patch, queueType, tier):
    for championId in CHAMPION_DATA:
        output_file = MIDPOINT_FILE_BASE.format(championId=championId, patch=patch, queueType=queueType, rank=tier)
        with open(output_file, "w") as fp:
            json.dump(fp, CHAMPION_DATA[championId])


def pasteMidpointFilesTogether():
    for championId in CHAMPION_DATA:
        print championId


def parseMatchesData(matches_data):
    pass


def main():

    for region in REGIONS:
        try:
            api = RiotAPI(API_KEY, region=region)
        except NameError as e:
            print e
            sys.exit(1)

        for patch in PATCHES:
            for queueType in QUEUETYPES:
                for tier in RANKED_TIERS[queueType]:
                    constructChampionDict()
                    fileindex = 0
                    try:
                        while (True):
                            BASE_PATH = ""
                            if QUEUETYPES[queueType] = "ranked":
                                BASE_PATH = RANKED_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.remove(".", ""), fileregion=region, fileindex=fileindex)
                            else:
                                BASE_PATH = NORMAL_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.remove(".", ""), tier=tier, fileregion=region, filetier=tier.lower(), fileindex=fileindex)
                            print "reading from {}...".format(BASE_PATH)
                            with open(BASE_PATH, 'r') as fp:
                                matches_data = json.load(fp)
                                parseMatchesData(matches_data)
                            fileindex += 1
                    except IOError:
                        print "done reading tier:{} in queueType:{} in patch:{} in region:{}".format(tier, queueType, patch, region)
                    flushAllData(region, patch, queueType, tier)

    pasteMidpointFilesTogether()
    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
