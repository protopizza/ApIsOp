import json
import urllib

def main():
	with open('../data/static/items514.json', 'r') as fp:
		item_list = json.load(fp)

	total_count = len(item_list["data"])

	for key in item_list["data"]:
		urllib.urlretrieve("http://ddragon.leagueoflegends.com/cdn/5.11.1/img/item/"+key+".png", key+".jpg")
	# print(json.dumps(item_list["data"], sort_keys=True, indent=4, separators=(',',':')))

main()