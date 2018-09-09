import requests
import logging
import json
import io
#load properties

with open('nfls_config.json') as f:
    cfg=json.load(f)
print(cfg)

url='https://www.fantasyfootballnerd.com/service/nfl-teams/json/'+ str(cfg["properties"]["apiKey"])+ '/'
#data='
response = requests.get(url)
print(response.json())

with open(cfg["properties"]["nflTeamsFile"], 'w') as f:
    json.dump(response.json(),f,sort_keys=True, indent=4)


logging.basicConfig(level=logging.INFO)
logging.getLogger('requests').setLevel(logging.DEBUG)

