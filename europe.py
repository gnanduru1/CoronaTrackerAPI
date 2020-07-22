import requests
import csv
import re

italy_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
uk_url = "https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-cases-uk.csv"
spain_url = "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
france_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'
departments_file = 'departments.txt'


def parse_csv_italy(url):
    with requests.Session() as s:
        response = []
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list[1:]:
            rowinfo = []
            province = row[5]  # province

            unformatted_date = row[0]
            # reformat date
            month = unformatted_date[5:7]
            day = unformatted_date[8:10]
            year = unformatted_date[0:4]
            date = '{0}-{1}-{2}'.format(year,month,day) # date

            country = row[1].replace('ITA', 'Italy')
            
            lat, lon = row[7], row[8]

            if not lat or not lon: 
                continue 
            if lat == "0.0" and lon == "0.0":  # region hasn't been defined yet, dont add to list
                continue
            if row[9]:
                confirmed = int(row[9])
            else:
                confirmed = 0

            rowinfo = [province, country, lat, lon, date, confirmed]
            response.append(rowinfo)  # add all rowinfo to list
        return response


def parse_csv_uk(url):
    with requests.Session() as s:
        response = []
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list[1:]:
            rowinfo = []
            province = row[3]  # province

            unformatted_date = row[0]
            # reformat date
            month = unformatted_date[5:7]
            day = unformatted_date[8:10]
            year = unformatted_date[0:4]
            date = '{0}-{1}-{2}'.format(year,month,day)  # date

            country = row[1]

            confirmed = row[4]
            if ' ' in confirmed:
                # for the ones that say (# to #)
                confirmed = re.findall('^\d+', confirmed)[0]
            confirmed = int(confirmed) if confirmed != 'NaN' and confirmed != '' else 'NaN'
            rowinfo = [province, country, 'und', 'und', date, confirmed]
            response.append(rowinfo)  # add all rowinfo to list
        return response


def parse_csv_spain(url):
    with requests.Session() as s:
        response = []
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list[1:]:
            rowinfo = []
            province = row[0]  # province

            unformatted_date = row[1]
            # reformat date
            month = unformatted_date[5:7]
            day = unformatted_date[8:10]
            year = unformatted_date[0:4]
            date = '{0}-{1}-{2}'.format(year,month,day)  # date

            country = 'Spain'

            if row[2]:
                # because this is a string with a decimal
                confirmed = int(row[2].replace('.0', ''))
            else:
                continue  # no confirmed data so don't add to regioninfo

            rowinfo = [province, country, 'und', 'und', date, confirmed]
            response.append(rowinfo)  # add all rowinfo to list
        return response


def parse_csv_france(url):
    departmentLOOKUP = {}
    # add department ids to lookup
    with open(departments_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            departmentID = re.findall(r'\d+', line)[0]
            province = re.findall(r' - [\w-]+', line)[0][3:]
            departmentLOOKUP[departmentID] = province

    with requests.Session() as s:
        response = []
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        # THIS CSV USES SEMICOLONS INSTEAD OF COMMAS
        cr = csv.reader(decoded_content.splitlines(), delimiter=';')
        my_list = list(cr)
        for row in my_list[1:]:
            rowinfo = []
            departmentID = row[0]
            if departmentID in departmentLOOKUP:
                province = departmentLOOKUP[departmentID]
            else:
                continue

            unformatted_date = row[2]
            # reformat date
            month = unformatted_date[5:7]
            day = unformatted_date[8:10]
            year = unformatted_date[0:4]
            date = '{0}-{1}-{2}'.format(year,month,day)  # date

            country = 'France'
            if row[3] and row[4]:
                confirmed = int(row[3]) + int(row[4])  # hosp + rea
            else:
                continue

            rowinfo = [province, country, 'und', 'und', date, confirmed]
            response.append(rowinfo)  # add all rowinfo to list
        return response


def write_csv(filename, data):
    fields = ['Province', 'Country', 'Lat', 'Lon', 'Date', 'Confirmed']
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        csvwriter.writerows(data)


def crawl():
    italy_data = parse_csv_italy(italy_url)
    write_csv("italy_data.csv", italy_data)
    print("italy_data.csv downloaded")

    uk_data = parse_csv_uk(uk_url)
    write_csv("uk_data.csv", uk_data)
    print("uk_data.csv downloaded")

    spain_data = parse_csv_spain(spain_url)
    write_csv("spain_data.csv", spain_data)
    print("spain_data.csv downloaded")

    france_data = parse_csv_france(france_url)
    write_csv("france_data.csv", france_data)
    print("france_data.csv downloaded")

    europe_data = italy_data + uk_data + spain_data + france_data
    write_csv('europe_data.csv', europe_data)
    print('europe_data.csv downloaded')

if __name__ == '__main__':
    crawl()
