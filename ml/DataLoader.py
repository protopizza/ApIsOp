import json
import numpy
import ModelGlobals

class DataLoader(object):

    NORMAL_INPUT_PATH_BASE = "../MATCH_DATA/{patch}/NORMAL_5X5/{region}/{filepatch}-normal-{fileregion}-{fileindex}.json"
    RANKED_INPUT_PATH_BASE = "../MATCH_DATA/{patch}/RANKED_SOLO/{region}/{tier}/{filepatch}-ranked-{fileregion}-{filetier}-{fileindex}.json"

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
    MAX_ITEMS = 6


    def __init__(self):
        pass


    def getMatch(self):
        for region in DataLoader.REGIONS:
            for patch in DataLoader.PATCHES:
                for queueType in DataLoader.QUEUETYPES:
                    for tier in DataLoader.RANKED_TIERS[queueType]:
                        TIER_LIST = []
                        if tier == "DIAMOND+":
                            TIER_LIST = DataLoader.DIAMOND_PLUS
                        else:
                            TIER_LIST.append(tier)
                        for destination_tier in TIER_LIST:
                            fileindex = 0
                            try:
                                while (True):
                                    BASE_PATH = ""
                                    if DataLoader.QUEUETYPES[queueType] == "ranked":
                                        BASE_PATH = DataLoader.RANKED_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), tier=destination_tier, fileregion=region, filetier=destination_tier.lower(), fileindex=fileindex)
                                    else:
                                        BASE_PATH = DataLoader.NORMAL_INPUT_PATH_BASE.format(patch=patch, region=region, filepatch=patch.replace(".", ""), fileregion=region, fileindex=fileindex)
                                    with open(BASE_PATH, 'r') as fp:
                                        matches_data = json.load(fp)
                                        for sequence in matches_data:
                                            matches_data[sequence]["matchTier"] = tier
                                            yield matches_data[sequence]
                                    fileindex += 1
                            except IOError:
                                pass



    def filterMatchFields(self, match):
        participants = match["participants"]
        match["patch"] = '.'.join(match["matchVersion"].split('.')[:2])
        desired_keys = [
            "matchTier",
            "patch"
            #"region"
        ]
        match = { key: match[key] for key in desired_keys}

        stats = []
        for player in participants:
            stats.append(player["stats"])
            player["stats"]["championId"] = player["championId"]
            if player["teamId"] == 100:
                player["stats"]["teamId"] = "A"
            else:
                player["stats"]["teamId"] = "B"

        teamA = []
        teamB = []

        for player in stats:
            if player["teamId"] == "A":
                teamA.append(player)

            else:
                teamB.append(player)

        if teamA[0]["winner"]:
            match['winnerTeamA'] = True
        else:
            match['winnerTeamA'] = False

        teamA = [player["championId"] for player in teamA]
        teamB = [player["championId"] for player in teamB]
        teamA.sort()
        teamB.sort()

        match['teamA'] = teamA
        match['teamB'] = teamB

        return match

