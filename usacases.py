from geopy.geocoders import Nominatim
# import pandas as pd
import csv, requests
from collections import OrderedDict
def convertDate(date):
    #no dash date to dashed date
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

def crawl():
    #state, country, lat, long, date, confirmed, dead, recovered
    geolocator = Nominatim(user_agent="coronatracker", timeout=5)

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
    LONLAT = {'Washington': (38.8948932, -77.0365529), 'Illinois': (40.0796606, -89.4337288),
              'California': (36.7014631, -118.7559974), 'Arizona': (34.395342, -111.7632755),
              'Massachusetts': (42.3788774, -72.032366), 'Wisconsin': (44.4308975, -89.6884637),
              'Texas': (31.8160381, -99.5120986), 'Nebraska': (41.7370229, -99.5873816),
              'Utah': (39.4225192, -111.7143584), 'Oregon': (43.9792797, -120.737257),
              'Florida': (27.7567667, -81.4639835), 'New York': (40.7127281, -74.0060152),
              'Rhode Island': (41.7962409, -71.5992372), 'Georgia': (32.3293809, -83.1137366),
              'New Hampshire': (43.4849133, -71.6553992), 'North Carolina': (35.6729639, -79.0392919),
              'New Jersey': (40.0757384, -74.4041622), 'Colorado': (38.7251776, -105.6077167),
              'Maryland': (39.5162234, -76.9382069), 'Nevada': (39.5158825, -116.8537227),
              'Tennessee': (35.7730076, -86.2820081), 'Hawaii': (21.2160437, -157.975203),
              'Indiana': (40.3270127, -86.1746933), 'Kentucky': (37.5726028, -85.1551411),
              'Minnesota': (45.9896587, -94.6113288), 'Oklahoma': (34.9550817, -97.2684063),
              'Pennsylvania': (40.9699889, -77.7278831), 'South Carolina': (33.6874388, -80.4363743),
              'District of Columbia': (38.893661249999994, -76.98788325388196), 'Kansas': (38.27312, -98.5821872),
              'Missouri': (38.7604815, -92.5617875), 'Vermont': (44.5990718, -72.5002608),
              'Virginia': (37.1232245, -78.4927721), 'Connecticut': (41.6500201, -72.7342163),
              'Iowa': (41.9216734, -93.3122705), 'Louisiana': (30.8703881, -92.007126), 'Ohio': (40.2253569, -82.6881395),
              'Michigan': (43.6211955, -84.6824346), 'South Dakota': (44.6471761, -100.348761),
              'Arkansas': (35.2048883, -92.4479108), 'Delaware': (38.6920451, -75.4013315),
              'Mississippi': (32.9715645, -89.7348497), 'New Mexico': (34.5708167, -105.993007),
              'North Dakota': (47.6201461, -100.540737), 'Wyoming': (43.1700264, -107.5685348),
              'Alaska': (64.4459613, -149.680909), 'Maine': (45.709097, -68.8590201), 'Alabama': (33.2588817, -86.8295337),
              'Idaho': (43.6447642, -114.0154071), 'Montana': (47.3752671, -109.6387579),
              'Puerto Rico': (18.2214149, -66.41328179513847), 'Virgin Islands': (17.789187, -64.7080574),
              'Guam': (13.450125700000001, 144.75755102972062), 'West Virginia': (38.4758406, -80.8408415),
              'Northern Mariana Islands': (14.149020499999999, 145.21345248318923), 'American Samoa': (-14.289304, -170.692511)}

    # url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    responses = requests.get(url)
    wrapper = csv.reader(responses.text.strip().split('\n'))
    ONE = [wrap for wrap in wrapper]
    url = 'https://covidtracking.com/api/states.csv'
    responses2 = requests.get(url)
    wrapper2 = csv.reader(responses2.text.strip().split('\n'))
    TWO = [wrap for wrap in wrapper2]
    # url = 'https://covidtracking.com/api/states/daily.csv'
    # responses3 = requests.get(url)
    # wrapper3 = csv.reader(responses3.text.strip().split('\n'))
    # THREE = [wrap for wrap in wrapper3]
    
    STATE = OrderedDict() #{state: []} #state, country, lat, long, date, confirmed, dead, recovered
    DATE = OrderedDict()#(state, date) = [{confirmed}, {dead}]
    
    HEADERS = ONE[0]
    HEADERS2 = TWO[0]#use state[0], positive[1] (#cases), death[11] dateModified[17]
    # HEADERS3 = THREE[0]# date[0], state[1], positive[2], death[6], deathIncrease[12]
    for tpl in ONE[1:]: #for df
        state = tpl[1]
        if state not in STATE:
            STATE[state] = []
        if state not in LONLAT:
            location = geolocator.geocode(state)
            LONLAT[state] = (location.latitude, location.longitude)
        key = (state, tpl[0])
        if key not in DATE:
            DATE[key] = [set(), set()]
        DATE[key][0].add(tpl[-2])
        DATE[key][1].add(tpl[-1])
    if 'dateModified' in HEADERS2:
        for tpl in TWO[1:]:
            if not str(tpl[1]) or not str(tpl[11]):
                continue
            state = tpl[1]
            if state in ABB:
                state = ABB[state]
            if state not in STATE:
                STATE[state] = []
            if state not in LONLAT:
                location = geolocator.geocode(state)
                if not location: print(tpl)
                LONLAT[state] = (location.latitude, location.longitude)
            date = tpl[-4][:10]
            key = (state, date)
            if key not in DATE:
                DATE[key] = [set(), set()]
            DATE[key][0].add(tpl[1])
            DATE[key][1].add(tpl[11])
    # for tpl in THREE[1:]:
    #     if not str(tpl[2]) or not str(tpl[6]):
    #         continue
    #     state = tpl[1]
    #     if state in ABB:
    #         state = ABB[state]
    #     if state not in STATE:
    #         STATE[state] = []
    #     if state not in LONLAT:
    #         location = geolocator.geocode(state)
    #         LONLAT[state] = (location.latitude, location.longitude)
    #     date = convertDate(str(tpl[0]))
    #     key = (state, date)
    #     if key not in DATE:
    #         DATE[key] = [set(), set()]
    #     DATE[key][0].add(tpl[2])
    #     DATE[key][1].add(tpl[6])

    for state, date in DATE:
        STATE[state] += [(state, 'US', LONLAT[state][0], LONLAT[state][1], date, max(DATE[(state, date)][0]), max(DATE[(state, date)][1]), 0)]

    with open('usastates.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('State', 'Country', 'Latitude', 'Longitude', 'Date', 'Confirmed', 'Deaths', 'Recovered'))
        for state in STATE:
            for tpls in STATE[state]:
                if "American Samoa" in tpls: continue
                writer.writerow(tpls)
    print('usastates.csv downloaded')

if __name__ == '__main__':
    crawl()