from RiotAPI import RiotAPI, Request
import apiKey
import json

API_KEY = apiKey.API_KEY

STATIC_DATA_CHAMPIONS_PATH = "data/static/champions.json"
STATIC_DATA_ITEMS_511_PATH = "data/static/items511.json"
STATIC_DATA_ITEMS_514_PATH = "data/static/items514.json"
CHAMPION_OUTPUT_PATH = "ml/championMap.json"
ITEM_OUTPUT_PATH = "ml/itemMap.json"

CHAMPION_TABLE = {}

CHAMPION_LIST = []

with open(STATIC_DATA_CHAMPIONS_PATH, 'r') as fp:
    champ_data = json.load(fp)

CHAMPION_LIST = [championKey for championKey in champ_data["data"]]
CHAMPION_LIST.sort()

total = len(CHAMPION_LIST)

print "There are {} total champions.".format(total)

for champ_idx in range(len(CHAMPION_LIST)):
    CHAMPION_TABLE[CHAMPION_LIST[champ_idx]] = champ_idx

with open(CHAMPION_OUTPUT_PATH, 'w') as fp:
    json.dump(CHAMPION_TABLE, fp)

with open(STATIC_DATA_ITEMS_511_PATH, 'r') as fp:
    items_511_data = json.load(fp)

with open(STATIC_DATA_ITEMS_514_PATH, 'r') as fp:
    items_514_data = json.load(fp)

ITEMS_511_LIST = [itemId for itemId in items_511_data["data"]]
ITEMS_514_LIST = [itemId for itemId in items_514_data["data"]]

try:
    api_client = RiotAPI(API_KEY, region="NA")
except NameError as e:
    print e
    sys.exit(1)

for patch in ["5.11", "5.14"]:
    item_req_api = ["lol-static-data", "map"]
    item_req_params = {"version":"{}.1".format(patch)}
    req = Request(item_req_api, item_req_params)
    resp = api_client.call(req)

    for item in resp["data"]:
        if resp["data"][item]["mapName"] == "SummonersRift":
            print resp["data"][item]["unpurchasableItemList"]


print "==========================================="
print "In 511 / Not in 514"
for itemId in ITEMS_511_LIST:
    if itemId not in ITEMS_514_LIST:
        print itemId, items_511_data["data"][itemId]["name"]

print "==========================================="
print "In 514 / Not in 511"
for itemId in ITEMS_514_LIST:
    if itemId not in ITEMS_511_LIST:
        print itemId, items_514_data["data"][itemId]["name"]

print "==========================================="
print "Discrepancies"
for itemId in ITEMS_511_LIST:
    if itemId in ITEMS_514_LIST:
        if items_511_data["data"][itemId]["name"] != items_514_data["data"][itemId]["name"]:
            print "5.11:", itemId, items_511_data["data"][itemId]["name"], "5.14:", itemId, items_514_data["data"][itemId]["name"]



print "done"