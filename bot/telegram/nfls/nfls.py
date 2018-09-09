import requests
import logging
import json
import io

def init():
    #load properties
    with open('nfls_config.json') as f:
        cfg=json.load(f)
        return cfg

cfg = init()
def api_get(url, apiKey):
    return requests.get(url + apiKey + '/')

def getScoringSettings():
    with open('league_settings.json') as f:
        settings_json = json.load(f)
        return settings_json

def loadTeams():
    with open(cfg["properties"]["nflTeamsFile"], 'w') as f:
        response = requests.get(cfg["api"]["nflTeams"] + str(cfg["properties"]["apiKey"])+ '/')
        json.dump(response.json(),f,sort_keys=True, indent=4)

def loadSchedule(nflScheduleFile): 
    with open(cfg["properties"]["nflScheduleFile"], 'w') as f:
            response = api_get(cfg["api"]["nflSchedule"], cfg["properties"]["apiKey"])
            json.dump(response.json(),f,sort_keys=True, indent=4)

def getTeams():
    with open('nfl_teams.json') as f:
        teams=json.load(f)
        return teams

def getSchedule():
    nflScheduleFile=cfg["properties"]["nflScheduleFile"]
    loadSchedule(nflScheduleFile)
    with open(nflScheduleFile) as f:
        schedule=json.load(f)
    return schedule


logging.basicConfig(level=logging.INFO)
logging.getLogger('requests').setLevel(logging.DEBUG)

