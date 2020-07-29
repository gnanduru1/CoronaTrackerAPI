import json

fn = 'afghanistan.json'

with open(fn, 'rb') as f:
   data = json.load(f)

for polygon in data['features']:
   del polygon['geometry']['coordinates'][0][19::20]

with open('test' + fn, 'w') as f:
   json.dump(data, f)