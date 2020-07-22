import csv
import requests
import lxml.html as lh
from datetime import date
from os import path
import json
from datetime import datetime


exchange_url = "https://www.x-rates.com/table/?from=USD&amount=1"
exchange_file = 'exchange_rate_global.csv'
convertDict = {'AUD': 'Australian Dollar', 'BRL': 'Brazilian Real', 'BGN': 'Bulgarian Lev', 'CAD': 'Canadian Dollar', 'CNY': 'Chinese Yuan Renminbi',
               'HRK': 'Croatian Kuna', 'CZK': 'Czech Koruna', 'DKK': 'Danish Krone', 'EUR': 'Euro', 'HKD': 'Hong Kong Dollar',
               'HUF': 'Hungarian Forint', 'ISK': 'Icelandic Krona', 'INR': 'Indian Rupee', 'IND': 'Indonesian Rupiah',
               'ILS': 'Israeli Shekel', 'JPY': 'Japanese Yen', 'RKW': 'South Korean Won', 'MYR': 'Malaysian Ringgit', 'MXN': 'Mexican Peso',
               'NOK': 'Norwegian Krone', 'PHP': 'Philippine Peso', 'PLN': 'Polish Zloty', 'RON': 'Romanian New Leu', 'RUB': 'Russian Ruble',
               'SGD': 'Singapore Dollar', 'ZAR': 'South African Rand', 'SEK': 'Swedish Krona', 'CHF': 'Swiss Franc', 'THB': 'Thai Baht',
               'TRY': 'Turkish Lira', 'GBP': 'British Pound', 'IDR': 'Indonesian Rupiah', 'NZD': 'New Zealand Dollar', 'USD': 'USD', 'KRW': 'South Korean Won'}

def sort_by_date(csv_file):
    data = csv.reader(open(csv_file, 'r'))
    next(data)  # skip header
    data = sorted(data, key=lambda row: datetime.strptime(row[2], "%Y-%m-%d"))
    with open(csv_file, "w", newline="") as f:
        f.truncate()  # clear the csv
        writer = csv.writer(f)
        writer.writerow(["Currency"] + ["Exchange Rate To USD"] + ["%Y-%m-%d"])
        writer.writerows(data)
    
def crawl():
    today = date.today().strftime("%Y-%m-%d")

    exchangePage = requests.get(exchange_url)
    exchange_doc = lh.fromstring(exchangePage.content)
    tr_elements = exchange_doc.xpath(
        '//*[@id="content"]/div[1]/div/div[1]/div[1]/table[2]//tr')
    col = []
    for row in tr_elements[1:]:
        temp = []
        for t in row:
            name = t.text_content()
            temp.append(name)
        col.append(temp)

    currencyDict = {}
    let = 'w'
    if path.exists(exchange_file):
        let = 'a'
    with open(exchange_file, let, newline='') as csvfile:
        exWriter = csv.writer(csvfile, delimiter=',')
        if let == 'w':
            exWriter.writerow(
                ["Currency"] + ["Exchange Rate To USD"] + ["%Y-%m-%d"])
            r = requests.get(
                "https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-04-01&base=USD")
            f = r.json()
            for day in f['rates']:
                for currency in f['rates'][day]:
                    exWriter.writerow(
                        [convertDict[currency], f['rates'][day][currency], day])
        exWriter.writerow(["USD"] + ["1.00"] + [today])

        currencies = []
        for item in col:
            exWriter.writerow(item[:-1] + [today])
            currencyDict[item[0]] = float(item[1])
            currencies += [item[0]]
    print(exchange_file, 'downloaded')
    sort_by_date(exchange_file)
    return {today: currencyDict}





if __name__ == '__main__':
    crawl()
    
