import psycopg2
import json
import sys

fn = 'france_data'

conn = psycopg2.connect(database='covidtracker', user='postgres', password='.-.', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

with open(fn + '.json') as f:
   data = json.load(f)

q = 'INSERT INTO ' + fn + ' VALUES ( '

for c in data:
   print(c)
   for d in data[c]:
      sql = q
      cursor.execute(sql + '\'' + c + '\', ' + '\'' + d + '\', ' + str(data[c][d]['confirmed']) + ' )')

conn.commit()
conn.close()