import psycopg2
import json
import sys

fn = 'currency_country'

conn = psycopg2.connect(database='covidtracker', user='postgres', password='.-.', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

with open(fn + '.json') as f:
   data = json.load(f)

q = 'INSERT INTO ' + fn + ' VALUES ( '

for c in data['countries']['country']:
   print(c)
   sql = q
   for d in c:
      if d == 'capital': continue
      sql += '\'' + c[d] + '\', ' if d != 'population' else ' ' + c[d] + ', '
   cursor.execute(sql[:-2] + ' )')

conn.commit()
conn.close()