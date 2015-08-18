from RiotAPI import RiotAPI, Request
import apiKey
import json
import math
import os
import sys

API_KEY = apiKey.API_KEY

INPUT_PATH_BASE = "MATCH_DATA/{patch}/RANKED_SOLO/{region}/{filepatch}-ranked-{fileregion}-{fileindex}.json"
OUTPUT_PATH_BASE = "MATCH_DATA/{patch}/RANKED_SOLO/{region}/{league}/{filepatch}-ranked-{fileregion}-{filetier}-{fileindex}.json"

REGIONS = ["NA"] #["BR", "EUNE", "EUW", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]
PATCHES = ["5.11", "5.14"]

# can tweak these values for testing 1000/10/10 is correct
TOTAL_MATCH_FILES_PER_PATCH = 1000
MATCHES_PER_FILE = 10
PLAYERS_PER_MATCH = 10

MATCHES = {
    "BRONZE": {
        "index": 0,
        "data": {}
    },
    "SILVER": {
        "index": 0,
        "data": {}
    },
    "GOLD": {
        "index": 0,
        "data": {}
    },
    "PLATINUM": {
        "index": 0,
        "data": {}
    },
    "DIAMOND": {
        "index": 0,
        "data": {}
    },
    "MASTER": {
        "index": 0,
        "data": {}
    },
    "CHALLENGER": {
        "index": 0,
        "data": {}
    }
}


def printMatches():
    '''
        testing purposes
    '''
    for match_tier in MATCHES:
        print "{} index:{} len:{}".format(match_tier, MATCHES[match_tier]["index"], len(MATCHES[match_tier]["data"]))


def dumpMatchFile(tier, patch, region):
    '''
        we could infer the fileindex number from existing filenames but on subsequent runs this wouldn't work. so we'll store the index, increment it, and reset it when necessary
    '''
    fileindex = MATCHES[tier]["index"]
    output_path = OUTPUT_PATH_BASE.format(patch=patch, region=region, league=tier, filepatch=patch.replace(".", ""), fileregion=region.lower(), filetier=tier.lower(), fileindex=fileindex)
    MATCHES[tier]["index"] += 1

    print "dumping {} matches to {}".format(tier, output_path)
    with open(output_path, 'w') as fp:
        json.dump(MATCHES[tier]["data"], fp)


def addMatch(match, tier, patch, region):
    '''
        we'll be storing potentially 72 matches in memory, which I think is a little less than 150MB
        when the match count for a given tier reaches 11, we'll dump the 10 previous matches of that tier into the next filename possible, then add in the new match to the dict
        since matches won't be dumped to file until they reach 11, we'll use flushFinalMatches to flush out everything leftover at the end of each patch section
    '''
    # printMatches()
    if len(MATCHES[tier]["data"]) >= 10:
        dumpMatchFile(tier, patch, region)
        MATCHES[tier]["data"] = {}

    sequence = "sequence{}".format(len(MATCHES[tier]["data"]))
    MATCHES[tier]["data"][sequence] = match


def flushFinalMatches(patch, region):
    '''
        additionally, this also resets the MATCHES structure for each patch section
    '''
    for match_tier in MATCHES:
        if len(MATCHES[match_tier]["data"]) > 0:
            dumpMatchFile(match_tier, patch, region)
        MATCHES[match_tier]["index"] = 0
        MATCHES[match_tier]["data"] = {}


def convertRankToRawPoints(tier="", division=""):
    '''
        0 unranked
        1-5 bronze
        6-10 silver
        11-15 gold
        16 - 20 platinum
        21 - 25 diamond
        26 master
        27 challenger
    '''
    val = 0

    if tier == "UNRANKED":
        return 0
    if tier == "BRONZE":
        val = 1
    elif tier == "SILVER":
        val = 6
    elif tier == "GOLD":
        val = 11
    elif tier == "PLATINUM":
        val = 16
    elif tier == "DIAMOND":
        val = 21
    elif tier == "MASTER":
        return 26
    elif tier == "CHALLENGER":
        return 27

    if division == "V":
        val += 0
    elif division == "IV":
        val += 1
    elif division == "III":
        val += 2
    elif division == "II":
        val += 3
    elif division == "I":
        val += 4

    return val


def convertRawPointsToRank(points=0):
    '''
        not necessarily accurate but we'll count UNRANKED matches as BRONZE. I haven't seen any unranked matches and if there are any, there
        are very few of them
    '''
    if points == 0:
        return "BRONZE"
    elif points == 26:
        return "MASTER"
    elif points == 27:
        return "CHALLENGER"

    tier_points = (points - 1)/ 5
    if tier_points == 0:
        return "BRONZE"
    elif tier_points == 1:
        return "SILVER"
    elif tier_points == 2:
        return "GOLD"
    elif tier_points == 3:
        return "PLATINUM"
    elif tier_points >= 4:
        return "DIAMOND"


def main():

    for region in REGIONS:
        try:
            api = RiotAPI(API_KEY, region=region)
        except NameError as e:
            print e
            sys.exit(1)

        for patch in PATCHES:
            check_path = INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), fileregion=region.lower(), fileindex="0")
            if not os.path.isfile(check_path):
                print "no such path, skipping ({})".format(check_path)
                continue

            for fileindex in range(TOTAL_MATCH_FILES_PER_PATCH):
                input_path = INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), fileregion=region.lower(), fileindex=fileindex)
                print "reading from " + input_path
                with open(input_path, 'r') as fp:
                    match_data = json.load(fp)
                    for sequence in range(MATCHES_PER_FILE):
                        sequence_field = "sequence{}".format(sequence)
                        current_ids = []
                        for participantId in match_data[sequence_field]["participantIdentities"]:
                            current_ids.append("{}".format(participantId["player"]["summonerId"]))

                        league_req_api = ["league", "by-summoner", "entry"]
                        league_req_ids = {"summonerIds":current_ids}
                        req = Request(league_req_api, league_req_ids)
                        try:
                            resp = api.call(req)
                            '''
                                NOTE: a 404 indicates that the player is UNRANKED. However when requesting with 10 summonerIDs at once, they just don't return any response for that ID
                            '''
                        except Exception as e:
                            print e
                            sys.exit(1)
                        result = {}

                        for player_idx in range(PLAYERS_PER_MATCH):
                            if current_ids[player_idx] in resp:
                                result[current_ids[player_idx]] = convertRankToRawPoints(resp[current_ids[player_idx]][0]["tier"], resp[current_ids[player_idx]][0]["entries"][0]["division"])
                            else:
                                result[current_ids[player_idx]] = convertRankToRawPoints("UNRANKED")


                        '''
                            by default integers will evaluate division to the lower value e.g. 6/5 = 1

                            so we will convert to float and use the ceil of the result

                            this means that matches on the edge such as GOLD I vs PLAT V will side towards being marked as PLAT V
                        '''
                        avg = 0
                        for key, value in result.items():
                            avg += value
                        rounded_avg = int(math.ceil(float(avg) / float(PLAYERS_PER_MATCH)))

                        addMatch(match_data[sequence_field], convertRawPointsToRank(rounded_avg), patch, region)

            flushFinalMatches(patch, region)

    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
