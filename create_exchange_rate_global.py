import psycopg2
import json
import sys

fn = 'exchange_rate_global'

cols = {'currency': 'text', 'date': 'date', 'exchange_rate': 'double precision'}

conn = psycopg2.connect(database='covidtracker', user='postgres', password='._.', host='127.0.0.1', port='5432')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS " + fn)

sql = 'CREATE TABLE ' + fn + '( '
for c in cols:
   sql += c + ' ' + cols[c] + ', '
sql = sql[:-2] + ')'

cursor.execute(sql)

conn.commit()
conn.close()