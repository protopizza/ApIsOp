'''

We will use a method similar to champion data to get item data.

For now this is specific to AP items.

Sample json item output data:

{
  "4000": {
    "NA": {
      "5.11": {
        "NORMAL_5X5": {
          "NO_RANK": {}
        },
        "RANKED_SOLO": {
          "BRONZE": {
            "matchesCounted" 100,
            "matchesBought": 100,
            "matchesWon": 60,
            "winRate": 60,
            "buyPercentage": 10,
            "averageTimeBought": 9000
          },
          "SILVER": {},
          "GOLD": {},
          "PLATINUM": {},
          "DIAMOND+": {}
        }
      },
      "5.14": {
      }
    }
  }
}


'''

import json
import math
import os
import sys

NORMAL_INPUT_PATH_BASE = "MATCH_DATA/{patch}/NORMAL_5X5/{region}/{filepatch}-normal-{fileregion}-{fileindex}.json"
RANKED_INPUT_PATH_BASE = "MATCH_DATA/{patch}/RANKED_SOLO/{region}/{tier}/{filepatch}-ranked-{fileregion}-{filetier}-{fileindex}.json"
MIDPOINT_FILE_BASE = "data/item/{itemId}-{region}-{patch}-{queueType}-{rank}.json"
OUTPUT_PATH_BASE = "data/item/{itemId}.json"

STATIC_AP_ITEM_CHANGES_PATH = "data/static/ap_item_changes.json"

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
        "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND+"
    ]
}

DIAMOND_PLUS = ["DIAMOND", "MASTER", "CHALLENGER"]
MAX_MATCHES_PER_FILE = 10
PLAYERS_PER_MATCH = 10
POSSIBLE_ITEM_SLOTS = 6

MIDPOINT_FILES = []
ITEM_DATA = {}
CHANGED_AP_ITEMS = {}



def buildGlobalTables():
    global CHANGED_AP_ITEMS
    with open(STATIC_AP_ITEM_CHANGES_PATH, 'r') as fp:
        CHANGED_AP_ITEMS = json.load(fp)


def constructItemDict():
    global ITEM_DATA
    ITEM_DATA = {}
    for item in CHANGED_AP_ITEMS:
        ITEM_DATA[item] = {}

        ITEM_DATA[item]["matchesCounted"] = 0
        ITEM_DATA[item]["matchesBought"] = 0
        ITEM_DATA[item]["matchesWon"] = 0
        ITEM_DATA[item]["winRate"] = 0
        ITEM_DATA[item]["buyPercentage"] = 0
        ITEM_DATA[item]["averageTimeBought"] = 0


def calculateNewAverage(old_value, new_value, original_match_count):
    return (old_value * original_match_count + new_value) / (original_match_count + 1)


def genericMetricUpdate(itemId, metric, new_value, original_match_count):
    global ITEM_DATA
    old_value = ITEM_DATA[itemId][metric]
    ITEM_DATA[itemId][metric] = calculateNewAverage(old_value, new_value, original_match_count)


def checkSpecialItemCases(item):
    '''
        some items aren't bought, they are automatically converted to from a different item, so we'll replace with the old item id

        seraph's embrace -> archangel's staff

        muramana -> manamune

        i could build a structure to look these up but since they're hardcoded anyway i'll just put in the values
    '''
    if item == 3040:
        item = 3003
    elif item == 3042:
        item = 3004
    return item


def findTimeBought(match_timeline, participant, item):
    item = checkSpecialItemCases(item)
    for frame in match_timeline["frames"]:
        if "events" not in frame:
            continue
        for event in frame["events"]:
            if event["eventType"] != "ITEM_PURCHASED" or event["itemId"] != item or event["participantId"] != participant:
                continue
            else:
                return event["timestamp"]


def itemFilter(item, patch):
    ITEM_TABLE = {
        #upgraded tear items
        3003: 3040, #archangel's -> seraph's
        3004: 3042, #manamune -> muramana
    }

    if item in ITEM_TABLE:
        return ITEM_TABLE[item]
    return item


def parseMatchesData(matches_data, patch):
    global ITEM_DATA

    matches_counted = 0
    try:
        for sequence in range(MAX_MATCHES_PER_FILE):
            match = matches_data["sequence{}".format(sequence)]
            match_length = match["matchDuration"]
            match_timeline = match["timeline"]
            matches_counted += 1

            duplicate_items = []
            team_items = {"100":[], "200":[]}
            for participant in match["participants"]:
                participantId = participant["participantId"]
                stats = participant["stats"]
                timeline = participant["timeline"]

                items = {}
                for index in range(POSSIBLE_ITEM_SLOTS):
                    item = stats["item{}".format(index)]
                    item = itemFilter(item, patch)

                    if item == 0:
                        continue

                    time_bought = findTimeBought(match_timeline, participantId, item)
                    if time_bought == None:
                        time_bought = match_length * 1000 #milliseconds

                    items[item] = time_bought

                for item in items:
                    if str(item) not in ITEM_DATA:
                        continue
                    if item not in duplicate_items:
                        original_matches_bought = ITEM_DATA[str(item)]["matchesBought"]
                        ITEM_DATA[str(item)]["matchesBought"] = original_matches_bought + 1
                        duplicate_items.append(item)

                        if stats["winner"]:
                            ITEM_DATA[str(item)]["matchesWon"] += 1

                    ITEM_DATA[str(item)]["winRate"] = "{:0.2f}".format(float(ITEM_DATA[str(item)]["matchesWon"]) / float(ITEM_DATA[str(item)]["matchesBought"]) * 100)

                    ITEM_DATA[str(item)]["averageTimeBought"] = calculateNewAverage(ITEM_DATA[str(item)]["averageTimeBought"], items[item], ITEM_DATA[str(item)]["matchesBought"])


    except Exception as e:
        print "no more matches left in this file ({})".format(e)

    for item in ITEM_DATA:
        ITEM_DATA[item]["matchesCounted"] += matches_counted
        ITEM_DATA[item]["buyPercentage"] = "{:0.2f}".format(float(ITEM_DATA[str(item)]["matchesBought"]) / float(ITEM_DATA[str(item)]["matchesCounted"]) * 100)


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
                parseMatchesData(matches_data, patch)
            fileindex += 1
    except IOError:
        print "done reading tier:{} in queueType:{} in patch:{} in region:{}".format(tier, queueType, patch, region)


def flushAllData(region, patch, queueType, destination_tier):
    global MIDPOINT_FILES
    for itemId in ITEM_DATA:
        output_file = MIDPOINT_FILE_BASE.format(itemId=itemId, region=region, patch=patch, queueType=queueType, rank=destination_tier)
        print "dumping to {}".format(output_file)
        with open(output_file, 'w') as fp:
            json.dump(ITEM_DATA[itemId], fp)
            MIDPOINT_FILES.append(output_file)


def pasteMidpointFilesTogether():
    for itemId in ITEM_DATA:
        itemData = {}
        for region in REGIONS:
            itemData[region] = {}
            for patch in PATCHES:
                itemData[region][patch] = {}
                for queueType in QUEUETYPES:
                    itemData[region][patch][queueType] = {}
                    for tier in RANKED_TIERS[queueType]:
                        itemData[region][patch][queueType][tier] = {}
                        input_file = MIDPOINT_FILE_BASE.format(itemId=itemId, region=region, patch=patch, queueType=queueType, rank=tier)
                        # print "reading from midpoint file:{}...".format(input_file)

                        try:
                            with open(input_file, 'r') as fp:
                                json_data = json.load(fp)
                                itemData[region][patch][queueType][tier] = json_data
                        except IOError:
                            print "no data for {} in {}/{}/{}/{}".format(itemId, tier, queueType, patch, region)

        output_file = OUTPUT_PATH_BASE.format(itemId=itemId)
        with open(output_file, 'w') as fp:
            json.dump(itemData, fp)


def cleanupMidpointFiles():
    for f in MIDPOINT_FILES:
        print "cleaning up {}...".format(f)
        os.remove(f)
    print "done cleaning"


def main():

    buildGlobalTables()

    for region in REGIONS:
        for patch in PATCHES:
            for queueType in QUEUETYPES:
                for tier in RANKED_TIERS[queueType]:
                    constructItemDict()
                    if tier == "DIAMOND+":
                        for destination_tier in DIAMOND_PLUS:
                            readFilesByType(region, patch, queueType, destination_tier)
                    else:
                        readFilesByType(region, patch, queueType, tier)
                    flushAllData(region, patch, queueType, tier)


    pasteMidpointFilesTogether()
    cleanupMidpointFiles()
    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
