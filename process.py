import os, csv, json, io
import who, europe, asia, usa
import econ, stocks, color
from shutil import copyfile

convertDictOld = {'Dominican Rep.': 'Dominican Republic',
 'Greenland-Denmark': '-Greenland',
 'Taiwan*': 'Taiwan',
 'Central African Rep.': 'Central African Republic',
 "Cote d'Ivoire": 'Ivory Coast',
 "Cote d%Ivoire": 'Ivory Coast',
 "Cote d&Ivoire": 'Ivory Coast',
 'Congo (Kinshasa)': 'Democratic Republic of the Congo',
 'Congo (Brazzaville)': 'Republic of the Congo',
 'Eq. Guinea': 'Equatorial Guinea',
 'S. Sudan': 'Sudan',
 'South Sudan': 'Sudan',
 'Bahamas': 'The Bahamas',
 'Virgin Islands-US': 'United States Virgin Islands',
 'Isle of Man-United Kingdom': 'Isle of Man',
 'American Samoa-US': 'American Samoa',
 'Bosnia and Herz.':'Bosnia and Herzegovina',
 'North Macedonia': 'Macedonia',
 'Aruba-Netherlands': 'Aruba',
 'French Polynesia-France': 'French Polynesia',
 'US': 'United States of America',
 'Puerto Rico-United States of America':'Puerto Rico',
 'NaN': '0',
 'Timor-Leste': 'East Timor',
 'Guinea-Bissau': 'Guinea Bissau',
 'Cabo Verde': 'Cape Verde',
 'Eswatini': 'Swaziland',
 'Burma': 'Myanmar',
 'Czechia': 'Czech Republic',
 'Czech Rep.': 'Czech Republic',
 'Korea, South': 'South Korea',
 'West Bank and Gaza': 'Palestine',
 'Holy See':'Vatican',

# uk countries labelled weirdly
 'England': 'United Kingdom',
 'Wales': 'United Kingdom',
 'Northern Ireland': 'United Kingdom',
 'Scotland': 'United Kingdom',
 'Diamond Princess': 'United Kingdom', # Cruise that technically belongs to UK, although it docked in California for medical help
 'MS Zaandam': 'United Kingdom', # British owned cruise
}

def cases():
    global bigDict, currencyTables, stockTables
    print('started')
    bigDict = {}

    bigDict.update(who.crawl())
    print('who')
    bigDict.update(europe.crawl()) 
    print('europe')   
    bigDict.update(asia.crawl())
    print('asia')
    bigDict.update(usa.crawl())
    print('usa')
                
    print("Initialized",len(bigDict),"regions")
    
    with io.open('global.json',mode='w',encoding='utf-8') as f:
        json.dump(bigDict,f,ensure_ascii=False)

def convert():
    for i in ['color.json', 'status.json', 'global.json']:
        text = open(i, 'r').read()
        for j in convertDict:
            text = text.replace(j, convertDict[j])
        f=open(i, 'w')
        f.write(text)
        f.close()
    print("Converted")

def customConfig(countries):
    custom = {}
    for i in countries:
        with open('countries/'+i+'.json', 'r') as f:
            custom[i] = json.load(f)
    with io.open('default.json', mode='w', encoding='utf-8') as f:
        json.dump(i, custom)

def moveFiles():
    for i in ['color.json', 'countries_110.json', 'currency_country.json', 'curr_code_to_name.json', 'default.json', 'exchange_rate_global.json', 'global.json', 'historic_stocks.json', 'status.json', 'stocks.json', 'stock_countries.json']:
        copyfile(i, 'data/'+i)

if __name__ == '__main__':
    cases()

    econ.crawl()
    stocks.crawl()
    color.crawl()    