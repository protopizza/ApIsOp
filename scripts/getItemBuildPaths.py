'''
    Generate item build paths for all items, getting all the possible build-into and build-from items (entire tree, not just parents/children)
    We can use this data to filter out lower tier items. Technically we only need into OR from to do this but might as well do both for completeness' sake
'''



from RiotAPI import RiotAPI, Request
import apiKey
import json

API_KEY = apiKey.API_KEY

OUTPUT_PATH = "data/static/item_build_paths.json"

PATCHES = ["5.11", "5.14"]

ITEM_BUILD_PATH_TABLE = {}

for patch in PATCHES:
    ITEM_BUILD_PATH_TABLE[patch] = {}

    try:
        api_client = RiotAPI(API_KEY, region="NA")
    except NameError as e:
        print e
        sys.exit(1)


    item_req_api = ["lol-static-data", "item"]
    item_req_params = {"version":"{}.1".format(patch), "itemListData":["from", "into"]}
    req = Request(item_req_api, item_req_params)
    resp = api_client.call(req)


    # build base table
    for itemId in resp["data"]:
        ITEM_BUILD_PATH_TABLE[patch][itemId] = {}
        ITEM_BUILD_PATH_TABLE[patch][itemId]["id"] = itemId
        ITEM_BUILD_PATH_TABLE[patch][itemId]["name"] = resp["data"][itemId]["name"]
        if "from" in resp["data"][itemId]:
            ITEM_BUILD_PATH_TABLE[patch][itemId]["from"] = resp["data"][itemId]["from"]
        else:
            ITEM_BUILD_PATH_TABLE[patch][itemId]["from"] = []
        if "into" in resp["data"][itemId]:
            ITEM_BUILD_PATH_TABLE[patch][itemId]["into"] = resp["data"][itemId]["into"]
        else:
            ITEM_BUILD_PATH_TABLE[patch][itemId]["into"] = []

# however we want all subcomponent items to be part of "from" and all final items to be part of "into", not just the direct child/parents in the tree
# items have a max depth of 4 (botrk for example)

for patch in PATCHES:
    for item in ITEM_BUILD_PATH_TABLE[patch]:

        # magic
        for from_item in ITEM_BUILD_PATH_TABLE[patch][item]["from"]:
            ITEM_BUILD_PATH_TABLE[patch][item]["from"].extend(ITEM_BUILD_PATH_TABLE[patch][from_item]["from"])
        ITEM_BUILD_PATH_TABLE[patch][item]["from"] = list(set(ITEM_BUILD_PATH_TABLE[patch][item]["from"]))

        for into_item in ITEM_BUILD_PATH_TABLE[patch][item]["into"]:
            ITEM_BUILD_PATH_TABLE[patch][item]["into"].extend(ITEM_BUILD_PATH_TABLE[patch][into_item]["into"])
        ITEM_BUILD_PATH_TABLE[patch][item]["into"] = list(set(ITEM_BUILD_PATH_TABLE[patch][item]["into"]))


with open(OUTPUT_PATH, 'w') as fp:
    json.dump(ITEM_BUILD_PATH_TABLE, fp, sort_keys=True, indent=4)


print "done"