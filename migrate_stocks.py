import psycopg2
import json
import sys

fn = 'stocks'

conn = psycopg2.connect(database='covidtracker', user='postgres', password='.-.', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

with open(fn + '.json') as f:
   data = json.load(f)

q = 'INSERT INTO ' + fn + ' VALUES ( '

for c in list(data[1:]):
   print(c)
   sql = q
   for i in c[:2]:
      sql += '\'' + i + '\', '
   for i in c[2:5]:
      sql += i.replace('%', '').replace(',', '') + ', '
   print(sql + '\'' + str(c[5]) + '\' )')
   cursor.execute(sql + '\'' + str(c[5]) + '\' )')

conn.commit()
conn.close()