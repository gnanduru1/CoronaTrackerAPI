import psycopg2
import json
import sys

fn = 'curr_code_to_name'

conn = psycopg2.connect(database='covidtracker', user='postgres', password='.-.', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

with open(fn + '.json', 'rb') as f:
   data = json.load(f)

q = 'INSERT INTO ' + fn + ' VALUES ( '

for c in data:
   print(c)
   sql = q + '\'' + c + '\' '
   for d in list(data[c])[:3]:
      sql += ', \'' + str(data[c][d]) + '\' '
   for d in list(data[c])[3:5]:
      sql += ', ' + str(data[c][d]) + ' '
   for d in list(data[c])[5:]:
      sql += ', \'' + str(data[c][d]) + '\' '
   cursor.execute(sql + ')')

conn.commit()
conn.close()