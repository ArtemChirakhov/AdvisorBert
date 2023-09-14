import json


f = open('data.json')
data = json.load(f)

print(len(data))