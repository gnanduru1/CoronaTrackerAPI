import requests, json
import lxml.html as lh
from datetime import date, datetime

exchange_url = "https://www.x-rates.com/table/?from=USD&amount=1"
exchange_file = 'exchange_rate_global.json'
convertDict = {'AUD': 'Australian Dollar', 'BRL': 'Brazilian Real', 'BGN': 'Bulgarian Lev', 'CAD': 'Canadian Dollar', 'CNY': 'Chinese Yuan Renminbi',
               'HRK': 'Croatian Kuna', 'CZK': 'Czech Koruna', 'DKK': 'Danish Krone', 'EUR': 'Euro', 'HKD': 'Hong Kong Dollar',
               'HUF': 'Hungarian Forint', 'ISK': 'Icelandic Krona', 'INR': 'Indian Rupee', 'IND': 'Indonesian Rupiah',
               'ILS': 'Israeli Shekel', 'JPY': 'Japanese Yen', 'RKW': 'South Korean Won', 'MYR': 'Malaysian Ringgit', 'MXN': 'Mexican Peso',
               'NOK': 'Norwegian Krone', 'PHP': 'Philippine Peso', 'PLN': 'Polish Zloty', 'RON': 'Romanian New Leu', 'RUB': 'Russian Ruble',
               'SGD': 'Singapore Dollar', 'ZAR': 'South African Rand', 'SEK': 'Swedish Krona', 'CHF': 'Swiss Franc', 'THB': 'Thai Baht',
               'TRY': 'Turkish Lira', 'GBP': 'British Pound', 'IDR': 'Indonesian Rupiah', 'NZD': 'New Zealand Dollar', 'USD': 'USD', 'KRW': 'South Korean Won'}

def sort_by_date(dct):
    newKeys = sorted(list(dct.keys()), key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    return {key:dct[key] for key in newKeys}
    
def crawl():
    econDict = {}   
    currencyDict = {}

    r = requests.get("https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-04-01&base=USD")
    f = r.json()
    for day in f['rates']:
        for currency in f['rates'][day]:
            if convertDict[currency] not in econDict:
                econDict[convertDict[currency]] = {day:f['rates'][day][currency]}
            else: 
                econDict[convertDict[currency]][day] = f['rates'][day][currency]

    for key in econDict: econDict[key] = sort_by_date(econDict[key])     
    with open('exchange_rate_global.json', 'w') as f: json.dump(econDict, f)
    print('econ')


if __name__ == '__main__':
    crawl()