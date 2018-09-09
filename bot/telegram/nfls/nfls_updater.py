#updater script for NFLS
import requests
import json
import time
import datetime
from shutil import copyfile

cfg = ''

def init():
    with open('nfls_config.json') as f:
       global  cfg 
       cfg = json.load(f)

def getTimestamp():
    return '{:%Y%m%d_%H:%M:%S}'.format(datetime.datetime.now())

def apiGet(url, apiKey):
    response = requests.get(url + apiKey + '/')
    return response.json()

def writeToFile(data_json,fileName):
    #create backup of last file
    #if fileName.isFile():
    #   copyfile(fileName, fileName + '_' +  getTimeStamp)
    with open(fileName, 'w') as f:
        json.dump(data_json, f, sort_keys=True, indent = 4)

#def updateSchedule():
    

def updateTeams():
    writeToFile(apiGet(cfg['api']['nflTeams'], cfg['properties']['apiKey']),cfg['properties']['nflTeamsFile'])

def updateFantasyScores():
    scores = apiGet(cfg['api']['nflScores'],'')
    for player in scores['players']:
        for team in player:
        team
        teamScoreFile = 'updates/nfl_scores' + team['teamAbbr'] + '.json'
        writeToFile(team, teamScoreFile)


def main():
    print("Starting Update")
    init()
    updateTeams()
    updateFantasyScores()

if __name__ == '__main__':
    main()
