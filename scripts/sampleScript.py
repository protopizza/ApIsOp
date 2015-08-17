from RiotAPI import RiotAPI, Request
import apiKey
import json
import sys

API_KEY = apiKey.API_KEY

def main():
    try:
        api = RiotAPI(API_KEY, region="north_america")
    except NameError as e:
        print e
        sys.exit(1)
    target_api = ["summoner", "by-name"]
    target_names = {"summonerNames":["aznchipmunk", "tovrikthethird", "omgnubness", "g0dzspeed"]}
    try:
        req = Request(target_api, target_names)
        get_summoner_response = api.call(req)
    except Exception as e:
        print e
        sys.exit(1)
    for name in target_names["summonerNames"]:
        print "{} (id {}):".format(get_summoner_response[name]["name"], get_summoner_response[name]["id"])
        target_api = ["league", "by-summoner", "entry"]
        target_args = {"summonerIds":get_summoner_response[name]["id"]}
        req = Request(target_api, target_args)
        try:
            response = api.call(req)
        except HTTPError, e:
            print e
            sys.exit(1)
        for item in response[str(get_summoner_response[name]["id"])]:
            if item["queue"] == "RANKED_SOLO_5x5":
                try:
                    latest_game = item["entries"][0]
                    print "Most recent match: {}, {} {}, {} LP".format(item["name"], item["tier"], latest_game["division"], latest_game["leaguePoints"])
                    try:
                        print "In series: {}".format(latest_game["miniSeries"]["progress"])
                    except:
                        print "Not in series."
                    print "Overall {}W / {}L, {:.2g}%".format(
                        latest_game["wins"],
                        latest_game["losses"],
                        float(100 * latest_game["wins"])/(latest_game["wins"] + latest_game["losses"]))
                except:
                    print "No match history found."


if __name__ == "__main__":
    main()
