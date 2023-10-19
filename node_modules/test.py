import json
import requests

f = open('data.json', 'w')
url = f"https://api.openalex.org/works?filter=from_publication_date:2020-01-01,cited-by-count:>20,has_abstract:true&per-page=20&cursor=*"
response = requests.get(url)
json_responce = response.json()
json.dump(json_responce['results'], f)

print(json_responce['results'])