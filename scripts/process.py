import os, csv, json, io, datetime
import who, europe, asia, usa
import econ, stocks, color
from shutil import copyfile

REACT_APP_LOCATION = 'C:/Users/Ganes/CoronaTracker/'

# Fix different sources calling the same country different names
convertDict = {'Tanzania': 'United Republic of Tanzania', 'Taiwan*': 'Taiwan', "Cote d'Ivoire": 'Ivory Coast', 'Congo (Kinshasa)': 'Democratic Republic of the Congo', 'Congo (Brazzaville)': 'Republic of the Congo', 'Bahamas': 'The Bahamas', 'North Macedonia': 'Macedonia', 'US': 'United States of America', 'Timor-Leste': 'East Timor', 'Guinea-Bissau': 'Guinea Bissau', 'Cabo Verde': 'Cape Verde', 'Eswatini': 'Swaziland', 'Burma': 'Myanmar', 'Czechia': 'Czech Republic', 'Korea, South': 'South Korea', 'West Bank and Gaza': 'Palestine', 'Holy See': 'Vatican'}
unmapped = {'Korea, North','Diamond Princess', 'MS Zaandam', 'Micronesia', 'Summer Olympics 2020', 'Winter Olympics 2022'}

def cases():
    global convertDict
    print('Started')
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
    
    smallDict = {}
    for i in bigDict.keys():
        lst = list(bigDict[i].items())
        lst = lst[::len(lst)//25 or 1]
        smallDict[i] = dict(lst)

    print("Initialized",len(bigDict),"regions")

    with io.open('../data/global.json',mode='w',encoding='utf-8') as f:
        json.dump(smallDict,f,ensure_ascii=False)
    
    with io.open('../data/all.json',mode='w',encoding='utf-8') as f:
        json.dump(bigDict,f,ensure_ascii=False)

    with open('../data/big_countries.json', 'w') as f:
        json.dump(list(big_countries), f)  

    customConfig(countries)
    createStatus(bigDict)

def createStatus(dct):
    status = {}
    for name in dct:
        status[name] = dct[name][list(dct[name].keys())[-1]]

    with io.open('../data/status.json', mode='w', encoding='utf-8') as f:
        json.dump(status, f)

def convert():
    for i in ['color.json', 'status.json', 'global.json']:
        with io.open('data/'+i, mode='r', encoding='utf-8') as f:
            text = f.read()
        for j in convertDict:
            text = text.replace(j, convertDict[j])
        with io.open('../data/'+i, mode='r', encoding='utf-8') as f:
            f.write(text)
    print("Converted")

def customConfig(countries):
    custom = {}
    for i in countries:
        with open('../countries/'+i+'.json', 'r') as f:
            custom[i] = json.load(f)
    with io.open('../data/default.json', mode='w', encoding='utf-8') as f:
        json.dump(custom, f)

def moveFiles():
    for i in ['color.json', 'countries_110.json', 'global.json', 'status.json', 'big_countries.json']:
        copyfile('../data/'+i, REACT_APP_LOCATION+'src/data/'+i)
    print('Moved files')

if __name__ == '__main__':
    cases()
    color.run()
    moveFiles() 