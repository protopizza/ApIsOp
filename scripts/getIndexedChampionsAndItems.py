from RiotAPI import RiotAPI, Request
import apiKey
import json

API_KEY = apiKey.API_KEY

STATIC_DATA_CHAMPIONS_PATH = "data/static/champions.json"
# STATIC_DATA_ITEMS_511_PATH = "data/static/items511.json"
# STATIC_DATA_ITEMS_514_PATH = "data/static/items514.json"
CHAMPION_OUTPUT_PATH = "ml/championMap.json"
# ITEM_OUTPUT_PATH = "ml/itemMap.json"

CHAMPION_TABLE = {}

CHAMPION_LIST = []

with open(STATIC_DATA_CHAMPIONS_PATH, 'r') as fp:
    champ_data = json.load(fp)

CHAMPION_LIST = [championKey for championKey in champ_data["data"]]
CHAMPION_LIST.sort()

CHAMPION_IDS = []
for champion in CHAMPION_LIST:
    CHAMPION_IDS.append(champ_data["data"][champion]["id"])


total = len(CHAMPION_IDS)

print "There are {} total champions.".format(total)

for champ_idx in range(len(CHAMPION_IDS)):
    CHAMPION_TABLE[CHAMPION_IDS[champ_idx]] = champ_idx

with open(CHAMPION_OUTPUT_PATH, 'w') as fp:
    json.dump(CHAMPION_TABLE, fp)




# with open(STATIC_DATA_ITEMS_511_PATH, 'r') as fp:
#     items_511_data = json.load(fp)

# with open(STATIC_DATA_ITEMS_514_PATH, 'r') as fp:
#     items_514_data = json.load(fp)

# ITEMS_511_LIST = [itemId for itemId in items_511_data["data"]]
# ITEMS_514_LIST = [itemId for itemId in items_514_data["data"]]

# try:
#     api_client = RiotAPI(API_KEY, region="NA")
# except NameError as e:
#     print e
#     sys.exit(1)

# unavailableItems = {}
# for patch in ["5.11", "5.14"]:
#     unavailableItems[patch] = []
#     item_req_api = ["lol-static-data", "item"]
#     item_req_params = {"version":"{}.1".format(patch), "itemListData":["maps"]}
#     req = Request(item_req_api, item_req_params)
#     resp = api_client.call(req)

#     for itemId in resp["data"]:
#         if "maps" in resp["data"][itemId]:
#             if "1" in resp["data"][itemId]["maps"]:
#                 unavailableItems[patch].append(itemId)

# ITEMS_511_LIST = [itemId for itemId in ITEMS_511_LIST if itemId not in unavailableItems["5.11"]]
# ITEMS_514_LIST = [itemId for itemId in ITEMS_514_LIST if itemId not in unavailableItems["5.14"]]


# BOOTS_DUPLICATES = {
#     3254: 1301, #berserker's greaves - alacrity
#     3274: 1326, #boots of mobility - alacrity
#     3284: 1306, #boots of swiftness - alacrity
#     3279: 1331, #ionian boots of ludicity - alacrity
#     3269: 1321, #mercury's treads - alacrity
#     3264: 1316, #ninja tabi - alacrity
#     3259: 1311, #sorcerer's shoes - alacrity
#     3251: 1302, #berserker's greaves - captain
#     3271: 1327, #boots of mobility - captain
#     3281: 1307, #boots of swiftness - captain
#     3276: 1332, #ionian boots of ludicity - captain
#     3266: 1322, #mercury's treads - captain
#     3261: 1317, #ninja tabi - captain
#     3256: 1312, #sorcerer's shoes - captain
#     3253: 1303, #berserker's greaves - distortion
#     3273: 1328, #boots of mobility - distortion
#     3283: 1308, #boots of swiftness - distortion
#     3278: 1333, #ionian boots of ludicity - distortion
#     3268: 1323, #mercury's treads - distortion
#     3263: 1318, #ninja tabi - distortion
#     3258: 1313, #sorcerer's shoes - distortion
#     3252: 1300, #berserker's greaves - furor
#     3272: 1325, #boots of mobility - furor
#     3282: 1305, #boots of swiftness - furor
#     3277: 1330, #ionian boots of ludicity - furor
#     3267: 1320, #mercury's treads - furor
#     3262: 1315, #ninja tabi - furor
#     3257: 1310, #sorcerer's shoes - furor
#     3250: 1304, #berserker's greaves - homeguard
#     3270: 1329, #boots of mobility - homeguard
#     3280: 1309, #boots of swiftness - homeguard
#     3275: 1334, #ionian boots of ludicity - homeguard
#     3265: 1324, #mercury's treads - homeguard
#     3260: 1319, #ninja tabi - homeguard
#     3255: 1314  #sorcerer's shoes - homeguard
# }


# '''
#     These discrepanies are the id changes of boot enchantments.
# '''
# # print "==========================================="
# # print "In 511 / Not in 514"
# # for itemId in ITEMS_511_LIST:
# #     if itemId not in ITEMS_514_LIST:
# #         if int(itemId) in BOOTS_DUPLICATES:
# #             print itemId, items_511_data["data"][itemId]["name"], BOOTS_DUPLICATES[int(itemId)], items_514_data["data"][str(BOOTS_DUPLICATES[int(itemId)])]["name"]
# #         else:
# #             print itemId, items_511_data["data"][itemId]["name"]


# '''
#     These discrepancies are solely black market brawlers items, sated devourer, and GP ult upgrades. We only need sated devourer.
# '''
# # print "==========================================="
# # print "In 514 / Not in 511"
# # for itemId in ITEMS_514_LIST:
# #     if itemId not in ITEMS_511_LIST:
# #         print itemId, items_514_data["data"][itemId]["name"]

# SATED_DEVOURER_IDS = ["3930", "3931", "3932", "3933"]


# '''
#     These discrepanies are magus -> runeglaive and the changing of Zeke's.
# '''
# # print "==========================================="
# # print "Discrepancies"
# # for itemId in ITEMS_511_LIST:
# #     if itemId in ITEMS_514_LIST:
# #         if items_511_data["data"][itemId]["name"] != items_514_data["data"][itemId]["name"]:
# #             print "5.11:", itemId, items_511_data["data"][itemId]["name"], "5.14:", itemId, items_514_data["data"][itemId]["name"]


# FINAL_ITEM_LIST = ITEMS_511_LIST + SATED_DEVOURER_IDS

# ITEM_TABLE = {}

# total_items = len(FINAL_ITEM_LIST)

# print "There are {} total items.".format(total_items)


# for item_idx in range(len(FINAL_ITEM_LIST)):
#     ITEM_TABLE[FINAL_ITEM_LIST[item_idx]] = item_idx


# with open(ITEM_OUTPUT_PATH, 'w') as fp:
#     json.dump(ITEM_TABLE, fp)


print "done"