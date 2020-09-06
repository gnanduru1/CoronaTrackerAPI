from geopy.geocoders import Nominatim
import pandas as pd
import csv, requests

ASIA = {
    'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh',
    'Bhutan', 'Brunei', 'Cambodia', 'China', 'Cyprus', 'Georgia',
    'India', 'Indonesia', 'Iran', 'Iraq', 'Israel',
    'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan',
    'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Burma',
    'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine',
    'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka',
    'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey',
    'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'
}

# state, country, lat, long, date, confirmed, dead, recovered
geolocator = Nominatim(user_agent="coronatracker", timeout=5)
LATLON = {}
REGIONS = {}

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
responseCASES = requests.get(url)
wrapperCASES = csv.reader(responseCASES.text.strip().split('\n'))
CASES = [wrap for wrap in wrapperCASES]

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
responseDEAD = requests.get(url)
wrapperDEAD = csv.reader(responseDEAD.text.strip().split('\n'))
DEATHS = [wrap for wrap in wrapperDEAD]
CHINA = {}

url = 'https://raw.githubusercontent.com/jihoo-kim/Data-Science-for-COVID-19/master/dataset/Time/TimeProvince.csv'
responseKOREA = requests.get(url)
wrapperKOREA = csv.reader(responseKOREA.text.strip().split('\n'))
KOREAREG = [wrap for wrap in wrapperKOREA]
KOREA = {}

url = 'https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/complete.csv'
responseINDIA = requests.get(url)
wrapperINDIA = csv.reader(responseINDIA.text.strip().split('\n'))
INDIAREG = [wrap for wrap in wrapperINDIA]
INDIA = {}

HEADERS = CASES[0]


def getDates(first, last):
    return [val.strftime('%Y-%m-%d') for val in pd.date_range(first, last)]


def crawl():
    DATES = getDates(HEADERS[4], HEADERS[-1])
    for cases, deaths in zip(CASES[1:], DEATHS[1:]):
        values = [*cases]  # [province/state, country/region, lat, long, cases]
        deathnums = [*deaths][4:]
        casesnums = [*cases][4:]
        province = str(values[0])
        country = values[1] if values[1] != 'Korea, South' else 'South Korea'
        key = (province, country) if province != 'nan' else ('', country)
        LATLON[key] = (values[2], values[3])
        REGIONS[key] = []
        for i in range(len(deathnums)):
            REGIONS[key] += [(*key, LATLON[key][0], LATLON[key][1], DATES[i], casesnums[i], deathnums[i], 0)]

    for values in INDIAREG[1:]:  # Date, _2(region), _5recovered, _6Latitude, _7Longitude,Death , _9confirmed
        date = values[0]
        region = values[1]
        key = (region, 'India')
        if key not in REGIONS:
            REGIONS[key] = []
            LATLON[key] = (values[5], values[6])
        REGIONS[key] += [(*key, LATLON[key][0], LATLON[key][1], date, values[-1], values[-2], values[4])]

    for values in KOREAREG[1:]:
        date = values[0]
        region = values[2]
        key = (region, 'South Korea')
        if key not in REGIONS:
            REGIONS[key] = []
            location = geolocator.geocode(region)
            LATLON[key] = (location.latitude, location.longitude)
        REGIONS[key] += [(*key, LATLON[key][0], LATLON[key][1], date, values[3], values[5], values[4])]
    
    toret = {}
    for state in REGIONS:
        key = state[0] + '-' + state[1]
        toret[key] = {}
        for tup in REGIONS[state]:
            toret[key][tup[4]] = tup[5]

    return toret


if __name__ == '__main__':
    crawl()
