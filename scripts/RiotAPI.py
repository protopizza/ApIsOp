import requests
import time
import string


class Request(object):
    def __init__(self, api_target, api_params={}):
        self.api = api_target
        self.params = api_params


class RiotAPI(object):

    URL = {
        "endpoint":"https://{host}.api.pvp.net/{api}",
        "status_endpoint":"http://status.leagueoflegends.com/{api}",
        "league":{
            "by-summoner":{
                "":"/api/lol/{region}/v{version}/league/by-summoner/{summonerIds}",
                "entry":"/api/lol/{region}/v{version}/league/by-summoner/{summonerIds}/entry"
                },
            "by-team":{
                "":"/api/lol/{region}/v{version}/league/by-team/{teamIds}",
                "entry":"/api/lol/{region}/v{version}/league/by-team/{teamIds}/entry"
            }
        },
        "lol-static-data":{
            "champion":{
                "":"/api/lol/static-data/{region}/v{version}/champion",
                "id":"/api/lol/static-data/{region}/v{version}/champion/{id}"
            },
            "item":{
                "":"/api/lol/static-data/{region}/v{version}/item",
                "id":"/api/lol/static-data/{region}/v{version}/item/{id}"
            }
        },
        "lol-status":{
            "shards":{
                "":"/shards",
                "region":"/shards/{region}"
            }
        },
        "match":{
            "":"/api/lol/{region}/v{version}/match/{matchId}",
        },
        "stats":{
            "by-summoner":{
                "ranked":"/api/lol/{region}/v{version}/stats/by-summoner/{summonerId}/ranked",
                "summary":"/api/lol/{region}/v{version}/stats/by-summoner/{summonerId}/summary"
            }
        },
        "summoner":{
            "by-name":"/api/lol/{region}/v{version}/summoner/by-name/{summonerNames}"
        }
    }


    API_VERSIONS = {
        "league":"2.5",
        "lol-static-data":"1.2",
        "lol-status":"1.0",
        "match":"2.2",
        "stats":"1.3",
        "summoner":"1.4"
    }


    REGIONS = {
        "global":"global",
        "brazil":"br",
        "europe_nordic_and_east":"eune",
        "europe_west":"euw",
        "korea":"kr",
        "latin_america_north":"lan",
        "latin_america_south":"las",
        "north_america":"na",
        "oceania":"oce",
        "turkey":"tr",
        "russia":"ru"
    }


    QUEUE_TYPES = [
        "RANKED_SOLO_5x5",
        "RANKED_TEAM_5x5"
    ]

    def __init__(self, api_key, region=REGIONS['global']):
        region = region.lower()
        self.api_key = api_key
        if region in RiotAPI.REGIONS:
            self.region = RiotAPI.REGIONS[region]
        elif region in RiotAPI.REGIONS.itervalues():
            self.region = region
        else:
            raise NameError("Error with region name.")


    def _requests(self, api_type, api_url, params, retries, retry_wait_seconds, retry_timeout_seconds):
        args = {"api_key": self.api_key}
        args.update(params.items())
        if api_type == "lol-status":
            full_req = RiotAPI.URL["status_endpoint"].format(
                host=self.region,
                api=api_url
            )
        elif api_type == "lol-static-data":
            full_req = RiotAPI.URL["endpoint"].format(
                host="global",
                api=api_url
            )
        else:
            full_req = RiotAPI.URL["endpoint"].format(
                host=self.region,
                api=api_url
            )

        got_response = False
        current_time = 0
        while not got_response:
            response = requests.get(full_req, params=args)
            if retries:
                if response.status_code == 429 or response.status_code >= 500:
                    if current_time >= retry_timeout_seconds:
                        raise Exception("call to {} timed out".format(full_req))
                    print "Error: {}, retrying in {} seconds".format(response.status_code, retry_wait_seconds)
                    time.sleep(retry_wait_seconds)
                    current_time += retry_wait_seconds
                else:
                    got_response = True
            else:
                break
        response.raise_for_status()
        return response.json()


    def call(self, request, retries=False, retry_wait_seconds=10, retry_timeout_seconds=1800):
        api_type = request.api[0]
        api_url = RiotAPI.URL
        for i in request.api:
            api_url = api_url[i]
        if isinstance(api_url, dict):
            api_url = api_url[""]
        args = {}
        args["region"] = self.region
        args["version"] = RiotAPI.API_VERSIONS[api_type]
        args.update(request.params.items())
        for key in args:
            if isinstance(args[key], list):
                args.update({key:','.join(args[key])})
        fields = [v[1] for v in string.Formatter().parse(api_url)]
        api_url = api_url.format(**args)
        for i in fields:
            if i in args:
                del args[i]
        try:
            return self._requests(api_type, api_url.lower(), args, retries, retry_wait_seconds, retry_timeout_seconds)
        except:
            raise
