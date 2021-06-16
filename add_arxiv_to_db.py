import argparse
import json

import arxiv
import requests

parser = argparse.ArgumentParser()

parser.add_argument('-s',
                    '--secret',
                    help='Get secret from Notion integrations')

parser.add_argument('-p', '--priority', help='Add reading priority of paper (high, medium or low)')

parser.add_argument('-url', '--url', help='paper url, either pdf or abs')

args = parser.parse_args()
paper_url = args.url
secret = args.secret
priority = args.priority.title()


paper_id = paper_url.split('/')[-1]
if 'pdf' in paper_id:
    paper_id = paper_id[:-4]

paper = next(arxiv.Search(id_list=[paper_id]).get())
year = paper.published.year
authors = [{"name": i.name} for i in paper.authors]
title = paper.title

url = paper_url
if "abs" in paper_url:
    url = f"https://arxiv.org/pdf/{paper_id}.pdf"

BASE_URL = "https://api.notion.com/v1/pages/"
NOTION_VERSION = "2021-05-13"

DB_ID = 'c0816a6c5f174cc688734de46d3511d2'

data = json.dumps({
    "parent": {
        "database_id": DB_ID
    },
    "properties": {
        "Authors": {
            "multi_select": authors
        },
        "Name": {
            "title": [{
                "text": {
                    "content": title
                }
            }]
        },
        "Year": {
            "number": year
        },
        "Progress": {
            "select": {
                "name": "Ready to start"
            }
        },
        "Priority": {
            "select": {
                "name": priority
            }
        },
        "URL": {
            "url": url
        }
    }
})

headers = {
    "Authorization": f"Bearer {secret}",
    "Notion-Version": f"{NOTION_VERSION}",
    "Content-Type": "application/json"
}

r = requests.post(BASE_URL, headers=headers, data=data)
print(r.status_code)
