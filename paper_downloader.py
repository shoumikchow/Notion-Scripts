import argparse
import json
import os

import requests
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-secret',
                    '--secret',
                    help='Get secret from Notion integrations')

args = parser.parse_args()
secret = args.secret

BASE_URL = "https://api.notion.com/v1/databases/"
NOTION_VERSION = "2021-05-13"

DB_ID = 'c0816a6c5f174cc688734de46d3511d2'

headers = {
    "Authorization": f"Bearer {secret}",
    "Notion-Version": f"{NOTION_VERSION}",
    "Content-Type": "application/json"
}

data = json.dumps({
    "filter": {
        "and": [{
            "property": "Progress",
            "select": {
                "equals": "Ready to start"
            }
        }, {
            "property": "Priority",
            "select": {
                "equals": "High"
            }
        }]
    },
    "sorts": [{
        "property": "Year",
        "direction": "ascending"
    }]
})

response = requests.post(BASE_URL + f'{DB_ID}' + '/query',
                         headers=headers,
                         data=data)
results = response.json()['results']

print(f"Retrieved {len(results)} from database")

if not os.path.exists('pdf'):
    os.makedirs('pdf')

for row in tqdm(results):
    properties = row['properties']

    name = properties['Name']['title'][0]['plain_text']
    year = properties['Year']['number']
    url = properties['URL']['url']

    r = requests.get(url, allow_redirects=True)
    extension = r.headers.get('content-type')

    if extension == "application/pdf":
        open(f'pdf/{year} - {name}', 'wb').write(r.content)
