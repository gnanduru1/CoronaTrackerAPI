from geopy.geocoders import Nominatim
import pandas as pd
import csv, requests
from io import StringIO

korea_url = 'https://raw.githubusercontent.com/jihoo-kim/Data-Science-for-COVID-19/master/dataset/Time/TimeProvince.csv'
india_url = 'https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/complete.csv'

def parse_csv_korea(url):
    return {}

def parse_csv_india(url):
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))    
        csvreader.__next__() # Skip the top line with all the headers
    dct = {}
    for row in csvreader:
        date = row[0]
        province = row[1]
        cases = int(float(row[4]))

        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}
    return dct

def crawl():
    asiaDict = {}    
    asiaDict.update(parse_csv_india(india_url))
    return asiaDict

if __name__ == '__main__':
    crawl()