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
              "123": {
                "isApItem": "yes",
                "buyPercentage": 80,
                "averageTimeBought": "15:00"
              },
              "456": {
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
STATIC_AP_ITEM_CHANGES = "data/static/ap_item_changes.json"


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
POSSIBLE_ITEM_SLOTS = 6 #exclude trinket
COMMON_ITEMS_TO_KEEP = 6

MIDPOINT_FILES = []
CHAMPION_ID_TABLE = {}
CHAMPION_DATA = {}

CHANGED_AP_ITEMS = {}


def buildChampionIdTable():
    global CHAMPION_ID_TABLE
    with open(STATIC_DATA_CHAMPIONS, 'r') as fp:
        static_champion_data = json.load(fp)

        for champion in static_champion_data["data"]:
            champId = static_champion_data["data"][champion]["id"]
            CHAMPION_ID_TABLE[champId] = champion
    global CHANGED_AP_ITEMS
    with open(STATIC_AP_ITEM_CHANGES, 'r') as fp:
        CHANGED_AP_ITEMS = json.load(fp)


def constructChampionDict():
    global CHAMPION_DATA
    CHAMPION_DATA = {}
    with open(STATIC_DATA_CHAMPIONS, 'r') as fp:
        static_champion_data = json.load(fp)

        for champion in static_champion_data["data"]:
            CHAMPION_DATA[champion] = {}

            CHAMPION_DATA[champion]["matchesCounted"] = 0
            CHAMPION_DATA[champion]["winRate"] = 0
            CHAMPION_DATA[champion]["matchesWon"] = 0
            CHAMPION_DATA[champion]["averageCsAt10"] = 0
            CHAMPION_DATA[champion]["averageCsPerMin"] = 0
            CHAMPION_DATA[champion]["averageGoldPerMin"] = 0
            CHAMPION_DATA[champion]["averageKda"] = 0
            CHAMPION_DATA[champion]["averageTotalDamageDealt"] = 0
            CHAMPION_DATA[champion]["averageTotalDamageDealtToChampions"] = 0
            CHAMPION_DATA[champion]["averageMagicDamageDealt"] = 0
            CHAMPION_DATA[champion]["averageMagicDamageDealtToChampions"] = 0
            CHAMPION_DATA[champion]["mostCommonItems"] = {}


def calculateNewAverage(old_value, new_value, original_match_count):
    return (old_value * original_match_count + new_value) / (original_match_count + 1)


def genericMetricUpdate(championKey, metric, new_value, original_match_count):
    global CHAMPION_DATA
    old_value = CHAMPION_DATA[championKey][metric]
    CHAMPION_DATA[championKey][metric] = calculateNewAverage(old_value, new_value, original_match_count)


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



def parseMatchesData(matches_data, destination_tier):
    global CHAMPION_DATA

    try:
        for sequence in range(MAX_MATCHES_PER_FILE):
            # print "====="
            match = matches_data["sequence{}".format(sequence)]
            match_length = match["matchDuration"]
            match_length_minutes = float(match_length) / 60
            match_timeline = match["timeline"]

            for participant in match["participants"]:
                participantId = participant["participantId"]
                championKey = CHAMPION_ID_TABLE[participant["championId"]]
                stats = participant["stats"]
                timeline = participant["timeline"]


                metric = "matchesCounted"
                original_matches_counted = CHAMPION_DATA[championKey][metric]
                CHAMPION_DATA[championKey][metric] = original_matches_counted + 1


                if stats["winner"]:
                    CHAMPION_DATA[championKey]["matchesWon"] += 1
                CHAMPION_DATA[championKey]["winRate"] = "{:0.2f}".format(float(CHAMPION_DATA[championKey]["matchesWon"]) / float(CHAMPION_DATA[championKey]["matchesCounted"]) * 100)



                metric = "averageCsAt10"
                new_value = timeline["creepsPerMinDeltas"]["zeroToTen"]
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageCsPerMin"
                raw = stats["minionsKilled"] + stats["neutralMinionsKilled"]
                new_value = float(raw)/float(match_length_minutes)
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageGoldPerMin"
                raw = stats["goldEarned"]
                new_value = float(raw)/float(match_length_minutes)
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageKda"
                deaths = stats["deaths"]
                if deaths == 0:
                    deaths = 1
                new_value = (float(stats["kills"]) + float(stats["assists"])) / float(deaths)
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageTotalDamageDealt"
                new_value = stats["totalDamageDealt"]
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageTotalDamageDealtToChampions"
                new_value = stats["totalDamageDealtToChampions"]
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageMagicDamageDealt"
                new_value = stats["magicDamageDealt"]
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)


                metric = "averageMagicDamageDealtToChampions"
                new_value = stats["magicDamageDealtToChampions"]
                genericMetricUpdate(championKey, metric, new_value, original_matches_counted)



                metric = "mostCommonItems"
                for index in range(POSSIBLE_ITEM_SLOTS):
                    item = stats["item{}".format(index)]
                    if item == 0:
                        continue

                    '''
                        Sometimes the purchasing of an item doesn't show up in the event history (excluding Muramana/Seraph's).
                        I'm not sure what causes this -- possibly buying the item right as the match is ending (due to killing nexus or surrender)
                        To work around this, I'll set the time bought to the match duration... alternatively we could just discard it
                    '''
                    time_bought = findTimeBought(match_timeline, participantId, item)
                    if time_bought == None:
                        # print "{} {} skipped, match {}, {}".format(participantId, item, match["matchId"], index)
                        # continue
                        time_bought = match_length * 1000 #milliseconds


                    if item in CHAMPION_DATA[championKey][metric]:
                        CHAMPION_DATA[championKey][metric][item]["buyCount"] += 1
                    else:
                        CHAMPION_DATA[championKey][metric][item] = {}
                        CHAMPION_DATA[championKey][metric][item]["id"] = item
                        CHAMPION_DATA[championKey][metric][item]["buyCount"] = 1
                        CHAMPION_DATA[championKey][metric][item]["averageTimeBought"] = 0
                        if str(item) in CHANGED_AP_ITEMS:
                            CHAMPION_DATA[championKey][metric][item]["isApItem"] = "yes"
                        else:
                            CHAMPION_DATA[championKey][metric][item]["isApItem"] = "no"

                    CHAMPION_DATA[championKey][metric][item]["buyPercentage"] = float(CHAMPION_DATA[championKey][metric][item]["buyCount"]) / float(CHAMPION_DATA[championKey]["matchesCounted"]) * 100

                    original_average_time_bought = CHAMPION_DATA[championKey][metric][item]["averageTimeBought"]
                    CHAMPION_DATA[championKey][metric][item]["averageTimeBought"] = calculateNewAverage(original_average_time_bought, time_bought, original_matches_counted)
                # print championKey, CHAMPION_DATA[championKey]
    except:
        print "no more matches left in this file"


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


def filterOnlyMostCommonItems(json_data):
    common_items = []
    data = {}
    for item in json_data["mostCommonItems"]:
        common_items.append(json_data["mostCommonItems"][item])
    common_items.sort(key=lambda x: x["buyPercentage"], reverse=True)
    for index in range(min(len(common_items), COMMON_ITEMS_TO_KEEP)):
        data[common_items[index]["id"]] = common_items[index]
    json_data["mostCommonItems"] = data
    return json_data


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
                                json_data = filterOnlyMostCommonItems(json_data)
                                championData[championKey][region][patch][queueType][tier] = json_data
                        except IOError:
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

    buildChampionIdTable()

    for region in REGIONS:
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


    pasteMidpointFilesTogether()
    cleanupMidpointFiles()
    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
