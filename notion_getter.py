from notion.client import NotionClient
import requests
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-cv', '--collection', help='enter URL of database')

parser.add_argument(
    '-token',
    '--token',
    help=
    'enter token_v2 from cookies (Developer Tools -> Application -> Storage -> Cookies'
)

args = parser.parse_args()
token = args.token
collection = args.collection

client = NotionClient(token_v2=token)
cv = client.get_collection_view(collection)

if not os.path.exists('pdf'):
    os.makedirs('pdf')

for row in tqdm(cv.collection.get_rows()):
    if row.Progress == "Ready to start" and row.Priority == "High":

        name = row.Name
        url = row.URL
        year = row.Year

        r = requests.get(url, allow_redirects=True)
        extension = r.headers.get('content-type')

        if extension == "application/pdf":
            open(f'pdf/{year} - {name}', 'wb').write(r.content)
