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
          "DIAMOND+": {}
        }
      },
      "5.14": {
        "NORMAL_5X5": {},
        "RANKED_SOLO": {
          "BRONZE": {},
          "SILVER": {},
          "GOLD": {},
          "PLATINUM": {},
          "DIAMOND+": {}
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
MIDPOINT_FILE_BASE = "data/champion/{championKey}-{region}-{patch}-{queueType}-{rank}.json"
OUTPUT_PATH_BASE = "data/champion/{championKey}.json"

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
    "NORMAL_5X5":[
        "NO_RANK"
    ],
    "RANKED_SOLO":[
        "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND+" #this order is important
    ]
}

DIAMOND_PLUS = ["DIAMOND", "MASTER", "CHALLENGER"]

MIDPOINT_FILES = []



def constructChampionDict():
    global CHAMPION_DATA
    CHAMPION_DATA = {}
    with open(STATIC_DATA_CHAMPIONS, 'r') as fp:
        static_champion_data = json.load(fp)

        for champion in static_champion_data["data"]:
            CHAMPION_DATA[champion] = {}
            CHAMPION_DATA[champion]["matchesCounted"] = 0
            CHAMPION_DATA[champion]["mostCommonItems"] = {}


def parseMatchesData(matches_data, destination_tier):
    global CHAMPION_DATA
    pass


def readFilesByType(region, patch, queueType, tier):
    fileindex = 0
    try:
        while (True):
            BASE_PATH = ""
            if QUEUETYPES[queueType] == "ranked":
                BASE_PATH = RANKED_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), tier=tier, fileregion=region, filetier=tier.lower(), fileindex=fileindex)
            else:
                BASE_PATH = NORMAL_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), fileregion=region, fileindex=fileindex)
            print "reading from {}...".format(BASE_PATH)
            with open(BASE_PATH, 'r') as fp:
                matches_data = json.load(fp)
                parseMatchesData(matches_data, tier)
            fileindex += 1
    except IOError:
        print "done reading tier:{} in queueType:{} in patch:{} in region:{}".format(tier, queueType, patch, region)


def flushAllData(region, patch, queueType, destination_tier):
    global MIDPOINT_FILES
    for championKey in CHAMPION_DATA:
        output_file = MIDPOINT_FILE_BASE.format(championKey=championKey, region=region, patch=patch, queueType=queueType, rank=destination_tier)
        print "dumping to {}".format(output_file)
        with open(output_file, 'w') as fp:
            json.dump(CHAMPION_DATA[championKey], fp)
            MIDPOINT_FILES.append(output_file)


def pasteMidpointFilesTogether():
    for championKey in CHAMPION_DATA:
        championData = {}
        championData[championKey] = {}
        for region in REGIONS:
            championData[championKey][region] = {}
            for patch in PATCHES:
                championData[championKey][region][patch] = {}
                for queueType in QUEUETYPES:
                    championData[championKey][region][patch][queueType] = {}
                    for tier in RANKED_TIERS[queueType]:
                        championData[championKey][region][patch][queueType][tier] = {}
                        input_file = MIDPOINT_FILE_BASE.format(championKey=championKey, region=region, patch=patch, queueType=queueType, rank=tier)
                        # print "reading from midpoint file:{}...".format(input_file)

                        try:
                            with open(input_file, 'r') as fp:
                                json_data = json.load(fp)
                                championData[championKey][region][patch][queueType][tier] = json_data[championKey]
                        except:
                            print "no data for {} in {}/{}/{}/{}".format(championKey, tier, queueType, patch, region)

        output_file = OUTPUT_PATH_BASE.format(championKey=championKey)
        with open(output_file, 'w') as fp:
            json.dump(championData, fp)


def cleanupMidpointFiles():
    for f in MIDPOINT_FILES:
        print "cleaning up {}...".format(f)
        os.remove(f)
    print "done cleaning"


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
                    if tier == "DIAMOND+":
                        for destination_tier in DIAMOND_PLUS:
                            readFilesByType(region, patch, queueType, destination_tier)
                    else:
                        readFilesByType(region, patch, queueType, tier)
                    flushAllData(region, patch, queueType, tier)
                    break
                break
            break


    pasteMidpointFilesTogether()
    cleanupMidpointFiles()
    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
