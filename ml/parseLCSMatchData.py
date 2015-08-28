import json

file_511 = "LCS_Matches_511.txt"
file_514 = "LCS_Matches_514.txt"

output_dir = "lcs_match_data"
output_file = "{patch}-{game}.json"

champion_static_data = "../data/static/champions.json"
CHAMPION_TABLE = {}

with open(champion_static_data, 'r') as fp:
    CHAMPION_TABLE = json.load(fp)

with open(file_511, 'r') as fp:
    current_match = {}
    gameName = ""
    name_base = ""
    name_match = ""
    patch = "5.11"
    winner = 0
    champList = []
    for line in fp.readlines():
        if line == "\n":
            continue
        elif "=" in line:
            continue
        elif "NA LCS" in line:
            continue
        else:
            if "Week" in line:
                name_base = line.lower().replace(",","").replace(" ","_")
            elif "Match" in line:
                splitline = line.split(":")
                name_match = splitline[0].strip().lower().replace(" ","_")
                name_match += "_" + splitline[1].strip().lower().replace(" ","_")
                winner = splitline[2]

            else:
                if "team" in line:
                    continue
                champList.append(CHAMPION_TABLE["data"][line.replace("\n","")]["id"])
                if len(champList) >= 10:
                    teamA = champList[:5]
                    teamB = champList[5:]
                    teamA.sort()
                    teamB.sort()
                    champList = []
                    current_match["teamA"] = teamA
                    current_match["teamB"] = teamB
                    if "teamA" in winner:
                        current_match["winnerTeamA"] = True
                    else:
                        current_match["winnerTeamA"] = False
                    current_match["patch"] = patch
                    current_match["matchTier"] = "DIAMOND+"
                    full_match_name = name_base.replace("\n", "") + "_" + name_match
                    with open(output_dir + '/' + output_file.format(patch=patch.replace(".",""), game=full_match_name), 'w') as outfile:
                        json.dump(current_match, outfile, indent=4)


with open(file_514, 'r') as fp:
    current_match = {}
    gameName = ""
    name_base = ""
    name_match = ""
    name_teams = ""
    patch = "5.14"
    winner = 0
    champList = []
    for line in fp.readlines():
        if line == "\n":
            continue
        elif "=" in line:
            continue
        elif "NA LCS" in line:
            continue
        else:
            if "final" in line.lower():
                splitline = line.split(":")
                name_base = splitline[0].strip().lower().replace(" ","_")
                name_teams = splitline[1].strip().lower().replace(" ","_")
            elif "third place" in line.lower():
                splitline = line.split(":")
                name_base = splitline[0].strip().lower().replace(" ","_")
                name_teams = splitline[1].strip().lower().replace(" ","_")
            elif "Match" in line:
                splitline = line.split(":")
                winner = splitline[1]
                name_match = splitline[0].lower().replace(" ","_")
            else:
                if "team" in line:
                    continue
                champList.append(CHAMPION_TABLE["data"][line.replace("\n","")]["id"])
                if len(champList) >= 10:
                    teamA = champList[:5]
                    teamB = champList[5:]
                    teamA.sort()
                    teamB.sort()
                    champList = []
                    current_match["teamA"] = teamA
                    current_match["teamB"] = teamB
                    if "teamA" in winner:
                        current_match["winnerTeamA"] = True
                    else:
                        current_match["winnerTeamA"] = False
                    current_match["patch"] = patch
                    current_match["matchTier"] = "DIAMOND+"
                    full_match_name = name_base.replace("\n", "") + "_" + name_match + "_" + name_teams
                    with open(output_dir + '/' + output_file.format(patch=patch.replace(".",""), game=full_match_name), 'w') as outfile:
                        json.dump(current_match, outfile, indent=4)

