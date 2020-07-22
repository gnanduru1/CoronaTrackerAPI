# process.py
# process CSV files into a data structure that can be called by server.py

import os, csv, json, time, math
from collections import OrderedDict
HEADERS = "Province/State,Country/Region,Lat,Long,Date,Confirmed,Dead,Recovered"
import simplejson
convertDict = {'Dominican Rep.': 'Dominican Republic',
 'Greenland-Denmark': 'Greenland',
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

class OrderedJsonEncoder( simplejson.JSONEncoder ):
    def encode(self,o):
        if isinstance(o, OrderedDict):
            return "{" + ",".join( [ self.encode(k)+":"+self.encode(o[k]) for i, k in enumerate(o) ] ) + "}"
        else:
            return simplejson.JSONEncoder.encode(self, o)


def parse_csv(filename):
    # TODO: update for compatibility with new CDC records
    records = OrderedDict()
    num = 0
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            num += 1
            if num == 1:
                continue
            providence = row[0]
            country = row[1]
            date = row[4]
            try:
                deaths = -1
                if len(row) > 6:
                    deaths = float(row[6])
                conf = float(row[5])
            except:
                #print(row)
                #print ("error on", filename)
                continue
                
            if len(providence) > 0:
                name = providence + "-" + country
            else:
                name = country
            if name not in records:
                records[name] = OrderedDict()
            if deaths != -1:
                records[name][date] = OrderedDict([('confirmed', conf), ('deaths', deaths)])
            else:
                records[name][date] = OrderedDict([('confirmed', conf)])
    return records


def init():
    global bigDict, currencyTables, stockTables
    
    bigDict = OrderedDict()
    currencyTables = {}
    stockTables = {}
    for name in ['asia.csv', 'europe_data.csv', 'france_data.csv', 'global.csv', 'italy_data.csv', 'spain_data.csv', 'uk_data.csv', 'usastates.csv', 'who_confirmed.csv']:
        bigDict.update(parse_csv(name))
    
    toDelete = []
    for place in bigDict:
        for date in bigDict[place]:
            if len(date) != 10:
                toDelete.append((place, date))
    for i in toDelete:
        del(bigDict[i[0]][i[1]])

    newDict = OrderedDict()
    for place in bigDict:
        temp = place.replace("'", "&").replace("*", "")
        if '-' in place:
            temp = place[(place.index("-"))+1:].replace("*", "")
        
        if temp not in newDict:
            newDict[temp] = OrderedDict()
        for date in bigDict[place]:
            if date not in newDict[temp]:
                if len(bigDict[place][date]) == 2:
                    newDict[temp][date] = OrderedDict([("confirmed", 0), ("deaths", 0)])
                else:
                    newDict[temp][date] = OrderedDict([("confirmed", 0)])
            for i in bigDict[place][date]:
                if i in newDict[temp][date]:
                    newDict[temp][date][i] += bigDict[place][date][i]
                    if math.isnan(bigDict[place][date][i]):
                        del newDict[temp][date]
                        break
    for place in bigDict:
        if place.replace("'", '%') not in newDict:
            go = True
            for date in bigDict[place]:
                for i in bigDict[place][date]:
                    if math.isnan(bigDict[place][date][i]):
                        go = False
            if go:
                newDict[place.replace("'", '%')] = bigDict[place]
    print("Initialized",len(newDict),"regions")
    e = OrderedJsonEncoder(newDict)
    f = open('global.json', 'w')
    file_str = e.encode(newDict).replace("'","%").replace("NaN","0")
    print(file_str.count("Canada"))
    f.write(file_str)
    f.close()

    f = open('global2.json', 'w')
    f.write(file_str)
    f.close()
                

def get(name, date):
    global bigDict
    if not bigDict: init()
    if name not in bigDict: return "Name not found"
    if date == 'all': return bigDict[name]
    if date not in bigDict[name]: return "Date out of range"
    return bigDict[name][date]

def keys():
    global bigDict
    return list(bigDict.keys())

def currency(currencyName):
    global currencyTables
    currencyTables = {}
    if not currencyTables:
        num = 0
        with open("exchange_rate_global.csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                num += 1
                if num == 1:
                    continue
                name = row[0]
                rate = float(row[1])
                date = row[2]
                if name not in currencyTables:
                    currencyTables[name] = {}
                currencyTables[name][date] = rate
    if currencyName == 'all': return currencyTables
    if currencyName in currencyTables: return currencyTables[currency]

def color(c, region):
    global colorTables
    callPlace = region.replace("'", '%') + '-' + c.replace("'", '%')
    if region == '-':
        callPlace = '-' + c.replace("'", '%')
    colorTables = {}     
    if not colorTables:
        with open("color.csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='#', quotechar='"')
            for row in spamreader:
                r = row[0].replace("'", '%')
                country = row[1].replace("'", '%')
                place = r + '-' + country
                color = row[2]
                status = row[3]
                if place not in colorTables:
                    colorTables[place] = {}
                colorTables[place] = color
    if c == 'all':
        return colorTables
    elif callPlace in colorTables: 
        return colorTables[callPlace]
    else:
        return "None"

def stocks(index):
    global stockTables
    # TODO: get daniel on this
    #return "Not implemented"
    stockTables = {}
    if not stockTables:
        num = 0
        with open("historic_stocks.csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                num += 1
                if num == 1:
                    continue
                name = row[0]
                rate = float(row[2].replace(',', ''))
                date = row[1]
                if name not in stockTables:
                    stockTables[name] = {}
                stockTables[name][date] = rate
    
    if index == 'all': return stockTables
    if index in stockTables: return stockTables[index]

def toJSON():
    # FILES = ['asia.csv', 'exchange_rate_global.csv', 'france_data.csv', 'italy_data.csv', 'spain_data.csv', 'stocks.csv', 'uk_data.csv', 'usastates.csv', 'who_confirmed.csv']
    FILES = [i for i in os.listdir() if ".csv" in i]
    for filename in FILES:
        jsonfilename = filename.replace('.csv', '.json')
        if filename == 'exchange_rate_global.csv':
            data = currency('all')
        elif filename == 'stocks.csv':
            data = stocks('all')
        elif filename == 'color.csv':
            data = color('all', 'all')
        elif filename == 'historic_stocks.csv':
            data = stocks('all')
        else:
            data = parse_csv(filename)
        with open(jsonfilename, 'w') as jsonfile:
            jsonfile.write(json.dumps(data, indent=4))
            
def status():
    # get the most recent data point for every region
    if not bigDict: return ""
    countries = {}
    entries = {}
    for name in bigDict:
        dates = bigDict[name].keys()
        try:
            myList = [time.strptime(date, r"%Y-%m-%d") for date in dates if '/' not in date]
        except:
            print(name)
            print(bigDict[name])
            print(dates)
            exit()
        if not myList: continue
        latest = max(myList) 
        entries[name] = bigDict[name][time.strftime(r"%Y-%m-%d",latest)]["confirmed"]
        ind = name.rfind("-")
        if ind != -1:
            country = name[ind+1:]
            if country in countries: countries[country] += entries[name]
            else: countries[country] = entries[name]

    entries.update(countries)
    with open("status.json", "w") as f:
        s = json.dumps(entries).replace("'",r"%").replace("NaN","0")
        f.write(s)

def bigCountries():
    global bigDict
    # get countries with regional data
    withRegions = {i[i.rfind('-')+1:] for i in bigDict if '-' in i}       
    with open("big_countries.json", "w") as f: 
        json.dump(list(withRegions), f)
    withRegions.update({i for i in bigDict if '-' not in i})
    with open("countries.json", "w") as f: 
        json.dump(list(withRegions), f)

def convert():
    for i in ['asia.csv', 'europe_data.csv', 'france_data.csv', 'global.csv', 'italy_data.csv', 'spain_data.csv', 'uk_data.csv', 'usastates.csv', 'who_confirmed.csv']:
        text = open(i, 'r').read()
        for j in convertDict:
            text = text.replace(j, convertDict[j])
        f=open(i, 'w')
        f.write(text)
        f.close()
    print("Converted")

def customConfig():
    customDict = {}
    with open("countries.json", 'r') as f:
        lst = json.load(f)
    # well not really a lst anymore
    lst = set(lst) | {i[:-5] for i in os.listdir('countries2')}
    for i in lst:
        try:
            with open("countries2/"+i+".json", 'r') as f:
                customDict[i] = json.load(f)
        except:
            with open("countries/"+i+".json", 'r') as f:
                customDict[i] = json.load(f)
    with open('custom.json', 'w') as f:
        json.dump(customDict,f)
    
    customDict = {}
    with open("big_countries.json", 'r') as f:
        lst = json.load(f)
    for i in lst:
        with open("big_countries/"+i+".json", 'r') as f:
            customDict[i] = json.load(f)
    with open('custom2.json', 'w') as f:
        json.dump(customDict,f)