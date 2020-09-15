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
convertDict = {'Tanzania': 'United Republic of Tanzania', 'Taiwan*': 'Taiwan', "Cote d'Ivoire": 'Ivory Coast', 'Congo (Kinshasa)': 'Democratic Republic of the Congo', 'Congo (Brazzaville)': 'Republic of the Congo', 'Bahamas': 'The Bahamas', 'North Macedonia': 'Macedonia', 'US': 'United States of America', 'Timor-Leste': 'East Timor', 'Guinea-Bissau': 'Guinea Bissau', 'Cabo Verde': 'Cape Verde', 'Eswatini': 'Swaziland', 'Burma': 'Myanmar', 'Czechia': 'Czech Republic', 'Korea, South': 'South Korea', 'West Bank and Gaza': 'Palestine', 'Holy See': 'Vatican'}
unmapped = {'Diamond Princess', 'MS Zaandam'}

def cases():
    global convertDict
    print('started')
    bigDict = {}
    countries = set()
    big_countries = set()
    lst = [bigDict, countries, big_countries]

    updates = lambda lst, lst2: [lst[i].update(lst2[i]) for i in range(len(lst))] 
    updates(lst, who.crawl())
    print('who')
    updates(lst, europe.crawl())
    print('europe')   
    updates(lst, asia.crawl())
    print('asia')
    updates(lst, usa.crawl())
    print('usa')
                
    # Fix data here
    keySet = set(bigDict.keys())
    for name in keySet:
        bigDict[name] = {k:v for _, (k,v) in enumerate(bigDict[name].items()) if v>0}
        if not bigDict[name]: del bigDict[name]

    for key in unmapped:
        if key in bigDict:
            del bigDict[key]
    countries -= unmapped
    big_countries -= unmapped

    for key in convertDict:
        if key in bigDict:
            bigDict[convertDict[key]] = bigDict.pop(key)
        if key in countries:
            countries.remove(key)
            countries.add(convertDict[key])
        if key in big_countries:
            big_countries.remove(key)
            big_countries.add(convertDict[key])

    print("Initialized",len(bigDict),"regions")

    with io.open('global.json',mode='w',encoding='utf-8') as f:
        json.dump(bigDict,f,ensure_ascii=False)

    with open('big_countries.json', 'w') as f:
        json.dump(list(big_countries), f)  

    customConfig(countries)
    createStatus(bigDict)

def createStatus(dct):
    status = {}
    for name in dct:
        status[name] = dct[name][list(dct[name].keys())[-1]]

    with io.open('status.json', mode='w', encoding='utf-8') as f:
        json.dump(status, f)

def convert():
    for i in ['color.json', 'status.json', 'global.json']:
        with io.open(i, mode='r', encoding='utf-8') as f:
            text = f.read()
        for j in convertDict:
            text = text.replace(j, convertDict[j])
        with io.open(i, mode='r', encoding='utf-8') as f:
            f.write(text)
    print("Converted")

def customConfig(countries):
    custom = {}
    for i in countries:
        with open('countries/'+i+'.json', 'r') as f:
            custom[i] = json.load(f)
    with io.open('default.json', mode='w', encoding='utf-8') as f:
        json.dump(custom, f)

def moveFiles():
    for i in ['color.json', 'countries_110.json', 'currency_country.json', 'curr_code_to_name.json', 'default.json', 'exchange_rate_global.json', 'global.json', 'historic_stocks.json', 'status.json', 'stocks.json', 'stock_countries.json', 'big_countries.json']:
        copyfile(i, 'data/'+i)

if __name__ == '__main__':
    cases()

    econ.crawl()
    stocks.crawl()
    color.crawl()

    moveFiles() 