from RiotAPI import RiotAPI, Request
import apiKey
import json
import math
import os
import sys

API_KEY = apiKey.API_KEY

NORMAL_INPUT_PATH_BASE = "MATCH_DATA/{patch}/NORMAL_5X5/{region}/{filepatch}-normal-{fileregion}-{fileindex}.json"
RANKED_INPUT_PATH_BASE = "MATCH_DATA/{patch}/RANKED_SOLO/{region}/{tier}/{filepatch}-ranked-{fileregion}-{filetier}-{fileindex}.json"
OUTPUT_PATH_BASE = "data/champion/{championName}.json"

'''
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
            "averageCsPerMin": 10,
            "averageGoldPerMin": 200,
            "averageKDA": 6,
            "averageDamageDealt": 14000,
            "mostCommonItems": {
              "item0": {
                "title": "Athene's Unholy Grail",
                "buyPercentage": 80,
                "averageTimeBought": "15:00"
              },
              "item1": {
                "title": "Rabadon's Deathcap",
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



REGIONS = ["NA"] #["BR", "EUNE", "EUW", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]
PATCHES = ["5.11", "5.14"]

RANKED_TIERS = ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "CHALLENGER"]

def main():

    for region in REGIONS:
        try:
            api = RiotAPI(API_KEY, region=region)
        except NameError as e:
            print e
            sys.exit(1)

        for patch in PATCHES:

    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
