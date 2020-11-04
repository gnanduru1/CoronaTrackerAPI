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
        country = row[1]
        if country == 'Georgia': country += ' (Country)'

        countries.add(country)
        if not row[0]:
            who_dict[country] = {dates[i]:int(row[i]) for i in range(4,len(row))}
        else:
            big_countries.add(country)
            who_dict[row[0]] = {dates[i]:int(row[i]) for i in range(4,len(row))}
            if country in who_dict:
                for date in who_dict[row[0]]: 
                    who_dict[country][date] += who_dict[row[0]][date]
            else:
                who_dict[country] = who_dict[row[0]].copy()
    return [who_dict, countries, big_countries]

if __name__ == '__main__':
    crawl()