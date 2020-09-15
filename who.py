import csv
import requests
from io import StringIO
import time
confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def crawl():
    with requests.get(confirmed_url) as data:
        csvreader = csv.reader(StringIO(data.text))
    dates = csvreader.__next__()
    who_dict = {}
    countries = {'Greenland'}
    big_countries = set()
    for row in csvreader:
        countries.add(row[1])
        if not row[0]:
            who_dict[row[1]] = {dates[i]:int(row[i]) for i in range(4,len(row))}
        else:
            big_countries.add(row[1])
            who_dict[row[0]] = {dates[i]:int(row[i]) for i in range(4,len(row))}
            if row[1] in who_dict:
                for date in who_dict[row[0]]: 
                    who_dict[row[1]][date] += who_dict[row[0]][date]
            else:
                who_dict[row[1]] = who_dict[row[0]].copy()

    return [who_dict, countries, big_countries]

if __name__ == '__main__':
    crawl()