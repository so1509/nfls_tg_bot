import nfls
import requests
import json
#for team in nfls.getTeams()["NFLTeams"]:
#    print(team["fullName"])

url = "http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season=2018&week=1&format=json"

response = requests.get(url)


with open('nfl_player.json', 'w') as f:
    json.dump(response.json(), f, sort_keys=True, indent = 4)

with open('nfl_player.json') as f:
    players = json.load(f)["players"]
    for player in players:
        with open(player["teamAbbr"] + '_player.json', 'a') as f:
            json.dump(player, f, sort_keys=True, indent = 4)
        
