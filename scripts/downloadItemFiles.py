import json
import urllib

def main():
	with open('../data/static/items514.json', 'r') as fp:
		item_list = json.load(fp)
	for key in item_list["data"]:
		urllib.urlretrieve("http://ddragon.leagueoflegends.com/cdn/5.14.1/img/item/"+key+".png", key+".jpg")
main()