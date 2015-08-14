from RiotAPI import Request, RiotAPI
import apiKey
import json
import sys

api_key = apiKey.api_key

input_path_base = "AP_ITEM_DATASET/{patch}/{queueType}/NA.json"
output_path_base = "MATCH_DATA/{patch}/{queueType}/NA/{sequence}.json"

patches = ["5.11", "5.14"]
queueTypes = ["NORMAL_5X5", "RANKED_SOLO"]

def main():
    try:
        api_client = RiotAPI(api_key, region="north_america")
    except NameError as e:
        print e
        sys.exit(1)

    match_req_api = ["match"]
    for patch in patches:
        for queueType in queueTypes:

            input_path = input_path_base.format(patch=patch, queueType=queueType)
            with open(input_path, 'r') as fp:
                input_matches = json.load(fp)

            for sequence in range(10):
                combined_resp = {}
                for i in range(10):
                    print "calling match api on id" + str(input_matches[i])
                    match_req_ids = {"matchId": str(input_matches[i]), "includeTimeline": "true"}
                    req = Request(match_req_api, match_req_ids)

                    try:
                        resp = api_client.call(req)
                    except Exception as e:
                        print e
                        sys.exit(1)
                    combined_resp["sequence" + str(i)] = resp

                output_path = output_path_base.format(patch=patch, queueType=queueType, sequence=sequence)
                print "dumping to " + output_path

                with open(output_path, 'w') as fp:
                    json.dump(combined_resp, fp)

    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
