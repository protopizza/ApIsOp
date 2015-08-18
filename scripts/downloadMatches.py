from RiotAPI import Request, RiotAPI
import apiKey
import json
import sys

API_KEY = apiKey.API_KEY

INPUT_PATH_BASE = "AP_ITEM_DATASET/{patch}/{queueType}/{region}.json"
OUTPUT_PATH_BASE = "MATCH_DATA/{patch}/{queueType}/{region}/{filepatch}-{filequeue}-{fileregion}-{fileindex}.json"

REGIONS = ["NA"] #["BR", "EUNE", "EUW", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]
PATCHES = ["5.11", "5.14"]
QUEUETYPES = {
    "NORMAL_5X5":"normal",
    "RANKED_SOLO":"ranked"
    }

MATCHES_PER_FILE = 10


def main():

    for region in REGIONS:

        try:
            api_client = RiotAPI(API_KEY, region=region)
        except NameError as e:
            print e
            sys.exit(1)

        match_req_api = ["match"]
        for patch in PATCHES:
            for queueType in QUEUETYPES:

                input_path = INPUT_PATH_BASE.format(patch=patch, queueType=queueType, region=region)
                with open(input_path, 'r') as fp:
                    input_matches = json.load(fp)

                total_count = len(input_matches)
                batch_count = total_count / MATCHES_PER_FILE
                print "{} input matches".format(len(input_matches))
                print "with {} matches per file, there will be {} batches".format(MATCHES_PER_FILE, batch_count)
                for fileindex in range(batch_count):
                    combined_resp = {}
                    for sequence in range(MATCHES_PER_FILE):
                        match_index = (fileindex * MATCHES_PER_FILE) + sequence
                        match_id = "{}".format(input_matches[match_index])

                        print "calling match api on id {}".format(match_id)
                        match_req_ids = {"matchId": match_id, "includeTimeline": "true"}
                        req = Request(match_req_api, match_req_ids)

                        try:
                            resp = api_client.call(req)
                        except Exception as e:
                            print e
                            sys.exit(1)
                        combined_resp["sequence{}".format(sequence)] = resp

                    output_path = OUTPUT_PATH_BASE.format(patch=patch, queueType=queueType, region=region, filepatch=patch.replace(".", ""), filequeue=QUEUETYPES[queueType], fileregion=region.lower(), fileindex=fileindex)
                    print "dumping to {}".format(output_path)

                    with open(output_path, 'w') as fp:
                        json.dump(combined_resp, fp)


    print "done"
    sys.exit(0)


if __name__ == "__main__":
    main()
