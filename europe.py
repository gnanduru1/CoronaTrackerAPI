import requests, csv, json
import re
from io import StringIO

italy_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
uk_url = "https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-cases-uk.csv"
spain_url = "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
france_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'
departments_file = 'departments.txt'


def parse_csv_italy(url):
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))    
        csvreader.__next__() # Skip the top line with all the headers
    dct = {}
    for row in csvreader:
        date = row[0][:10]
        province = row[5]
        cases = int(row[-2])

        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}
    return dct

def parse_csv_uk(url):
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))    
        csvreader.__next__()

    dct = {}
    for row in csvreader:
        if row[4] == 'NaN': continue
        cases = int(row[4])

        date = row[0]
        province = row[3]
        

        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}
    return dct
    
def parse_csv_spain(url):
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))
        csvreader.__next__()

    dct = {}
    for row in csvreader:
        if not row[2]: continue
        cases = int(float(row[2]))

        date = row[1]
        province = row[0]

        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}
    return dct
    
def parse_csv_france(url):
    regionLookup = {"01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes", "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube", "11": "Aude", "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal", "16": "Charente", "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud", "2B": "Haute-Corse", "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne", "25": "Doubs", "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère", "30": "Gard", "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault", "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura", "40": "Landes", "41": "Loir-et-Cher", "42": "Loire - St", "43": "Haute-Loire", "44": "Loire-Atlantique", "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire", "50": "Manche - St", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle", "55": "Meuse - Bar-le", "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord", "60": "Oise", "61": "Orne", "62": "Pas-de-Calais", "63": "Puy de Dôme", "64": "Pyrénées-Atlantiques", "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône", "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie", "75": "Paris", "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres", "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse", "85": "Vendeé", "86": "Vienne", "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne", "90": "Territoire de Belfort", "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne", "95": "Val-d'Oise", "971": "Guadeloupe", "972": "Martinique", "973": "Guyane", "974": "La-Reunion", "976": "Mayotte"}
    
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text), delimiter=';')    
        csvreader.__next__()

    dct = {}
    for row in csvreader:
        if not row[0]:
            continue
        province = regionLookup[row[0]]
        date = row[2]
        cases = int(row[3])+int(row[4])
        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}
    return dct
    
def crawl():
    print(parse_csv_spain(spain_url).keys())
    exit()

    all_data = {}
    all_data.update(parse_csv_italy(italy_url))
    all_data.update(parse_csv_uk(uk_url))
    all_data.update(parse_csv_spain(spain_url))
    all_data.update(parse_csv_france(france_url))

    return [all_data, {'France', 'Spain', 'Italy', 'United Kingdom'}, {'France', 'Spain', 'Italy', 'United Kingdom'}]

if __name__ == '__main__':
    crawl()