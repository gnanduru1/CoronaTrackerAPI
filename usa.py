import csv, requests
from io import StringIO

ABB = {
                    'AK': 'Alaska',
                    'AL': 'Alabama',
                    'AR': 'Arkansas',
                    'AS': 'American Samoa',
                    'AZ': 'Arizona',
                    'CA': 'California',
                    'CO': 'Colorado',
                    'CT': 'Connecticut',
                    'DC': 'District of Columbia',
                    'DE': 'Delaware',
                    'FL': 'Florida',
                    'GA': 'Georgia',
                    'GU': 'Guam',
                    'HI': 'Hawaii',
                    'IA': 'Iowa',
                    'ID': 'Idaho',
                    'IL': 'Illinois',
                    'IN': 'Indiana',
                    'KS': 'Kansas',
                    'KY': 'Kentucky',
                    'LA': 'Louisiana',
                    'MA': 'Massachusetts',
                    'MD': 'Maryland',
                    'ME': 'Maine',
                    'MI': 'Michigan',
                    'MN': 'Minnesota',
                    'MO': 'Missouri',
                    'MP': 'Northern Mariana Islands',
                    'MS': 'Mississippi',
                    'MT': 'Montana',
                    'NA': 'National',
                    'NC': 'North Carolina',
                    'ND': 'North Dakota',
                    'NE': 'Nebraska',
                    'NH': 'New Hampshire',
                    'NJ': 'New Jersey',
                    'NM': 'New Mexico',
                    'NV': 'Nevada',
                    'NY': 'New York',
                    'OH': 'Ohio',
                    'OK': 'Oklahoma',
                    'OR': 'Oregon',
                    'PA': 'Pennsylvania',
                    'PR': 'Puerto Rico',
                    'RI': 'Rhode Island',
                    'SC': 'South Carolina',
                    'SD': 'South Dakota',
                    'TN': 'Tennessee',
                    'TX': 'Texas',
                    'UT': 'Utah',
                    'VA': 'Virginia',
                    'VI': 'Virgin Islands',
                    'VT': 'Vermont',
                    'WA': 'Washington',
                    'WI': 'Wisconsin',
                    'WV': 'West Virginia',
                    'WY': 'Wyoming'
    }

def crawl():
    global ABB

    dct = {}
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))
        csvreader.__next__()

    dct = {}
    for row in csvreader:
        cases = int(row[3])
        date = row[0]
        date = date[5:7]+'/'+date[8:]+'/'+date[2:4]
        province = row[1]

        if province in dct: dct[province][date] = cases
        else: dct[province] = {date: cases}

    url = 'https://covidtracking.com/api/states/daily.csv'
    with requests.get(url) as data:
        csvreader = csv.reader(StringIO(data.text))
        csvreader.__next__()
    
    updated = 0
    for row in csvreader:
        if not row[2]: continue
        province = ABB[row[1]]
        date = row[0][4:6]+'/'+row[0][6:]+'/'+row[0][2:4]
        if province not in dct:
            dct[province] = {date:int(row[2])}
        elif date not in dct[province] or 'A' in row[12]:
            updated += 1
            dct[province][date] = int(row[2])
            
    return [dct, {'United States of America'}, {'United States of America'}]


if __name__ == '__main__':
    crawl()