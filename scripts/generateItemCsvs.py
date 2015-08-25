import json
import csv

STATIC_AP_ITEM_CHANGES_PATH = "data/static/ap_item_changes.json"
INPUT_PATH = "data/item/{itemId}.json"
OUTPUT_FILE = "data/viz/items.csv"

AA_STAFF = 3003

PATCHES = {
    "5.11",
    "5.14"
}

TIERS = [
    "NO_RANK",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "DIAMOND+"
]

FIELDS = [
    "WinRate",
    "BuyRate"
]

region = "NA" # only NA data


with open(STATIC_AP_ITEM_CHANGES_PATH, 'r') as fp:
    ap_items = json.load(fp)

with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile)

    column_names = ["ITEM_ID"]
    for patch in PATCHES:
        for tier in TIERS:
            for field in FIELDS:
                column_names.append("{}-{}-{}".format(patch.replace(".",""), tier, field))
    writer.writerow(column_names)

    item_ids = []
    for itemId in ap_items:
        if itemId != str(AA_STAFF):
            item_ids.append(itemId)

    item_ids.sort()

    for itemId in item_ids:
        row_values = []
        row_values.append(itemId)

        with open(INPUT_PATH.format(itemId=itemId)) as fp:
            item_json_data = json.load(fp)

        for patch in PATCHES:
            for tier in TIERS:
                if tier == "NO_RANK":
                    queueType = "NORMAL_5X5"
                else:
                    queueType = "RANKED_SOLO"
                row_values.append(item_json_data[region][patch][queueType][tier]["winRate"])
                row_values.append(item_json_data[region][patch][queueType][tier]["buyPercentage"])

        writer.writerow(row_values)

