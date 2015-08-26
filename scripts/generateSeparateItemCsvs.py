import json
import csv

STATIC_AP_ITEM_CHANGES_PATH = "data/static/ap_item_changes.json"
INPUT_PATH = "data/item/{itemId}.json"
OUTPUT_FILE_BASE = "data/viz/items-{patch}-{tier}-{field}.csv"

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

FIELDS = {
    "WinRate":"winRate",
    "BuyRate":"buyPercentage"
}

region = "NA" # only NA data


with open(STATIC_AP_ITEM_CHANGES_PATH, 'r') as fp:
    ap_items = json.load(fp)


for patch in PATCHES:
    for tier in TIERS:
        for field in FIELDS:
            output_file = OUTPUT_FILE_BASE.format(patch=patch.replace(".",""), tier=tier, field=field)

            with open(output_file, 'wb') as csvfile:
                writer = csv.writer(csvfile)

                column_names = ["ITEM_ID"]
                column_names.append(field)
                column_names.append("Not{}".format(field))

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

                    if tier == "NO_RANK":
                        queueType = "NORMAL_5X5"
                    else:
                        queueType = "RANKED_SOLO"
                    field_data = item_json_data[region][patch][queueType][tier][FIELDS[field]]
                    row_values.append(field_data)
                    oppositeRate = 100.0 - float(field_data)
                    row_values.append(float(str(oppositeRate)))

                    writer.writerow(row_values)

