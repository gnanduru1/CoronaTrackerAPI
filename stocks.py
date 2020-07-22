import csv, requests
#import lxml.html as lh
from datetime import date
from os import path
import json
import re

re_name = r'(?<=title=")(.*?)(?=")'
re_country = r'(?<=\n)[\w ]+(?=.*</td>)'
re_last = r'[\d.,]+(?=<br/>)'
re_change = r'(?<=>)[\d.-]+(?=</span><br/>)'
re_percent = r'(?<=>)[\d.-]+%(?=</span>)'

queries = [re_name,re_country,re_last,re_change,re_percent]

stock_url = "https://markets.businessinsider.com/indices"
stock_file = "stocks.json"
key_file = "stock_countries.json"

def crawl():
    today = date.today().strftime("%Y-%m-%d")

    stockPage = requests.get(stock_url)
    substr = r'<a class="deep-sea-blue'

    txt = stockPage.text
    txt = txt[txt.find(substr):]
    txt = txt[:txt.find('</table>')]
    
    entries = [entry for entry in txt.split(substr) if '>' in entry]
    results = []

    for entry in entries:
        results.append([re.search(query,entry).group(0) for query in queries]+[today])

    countries = {}
    for result in results:
        if result[1] in countries:
            countries[result[1]].append(result[0])
        else:
            countries[result[1]] = [result[0]]

    with open(key_file, "w") as f: json.dump(countries, f)
    with open(stock_file, "w") as f: json.dump([["Name","Country","Last","+/-",'%',"Date"]]+results,f)

if __name__ == '__main__':
    crawl()