import psycopg2
import json
import sys

fn = 'big_countries'

conn = psycopg2.connect(database='covidtracker', user='postgres', password='.-.', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

with open(fn + '.json') as f:
   data = json.load(f)

q = 'INSERT INTO ' + fn + ' VALUES ( '

for c in data:
   print(c)
   sql = q
   cursor.execute(sql + '\'' + c + '\' )')

conn.commit()
conn.close()