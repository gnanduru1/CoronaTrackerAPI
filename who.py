import csv
import requests

confirmed_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
confirmed_file = 'who_confirmed.csv'
def crawl():
    # Refresh CSV files from CDC
    # NOTE: parse_csv is outdated as of 3/26
    writer = open(confirmed_file, "w")
    writer.write(requests.get(confirmed_url).text)
    writer.close()

    dates = []
    csvArray = []
    with open(confirmed_file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row:
                csvArray.append(row)

    for d in csvArray[0][4:]:
        arr = d.split("/")
        if len(arr[0]) == 1:
            arr[0] = '0'+arr[0] 
        if len(arr[1]) == 1:
            arr[1] = '0'+arr[1] 
        if len(arr[2]) == 2:
            arr[2] = '20'+arr[2]
        dates.append(arr[2]+'-'+arr[0]+'-'+arr[1])
    del csvArray[0][4:]
    csvArray[0].append("Date")

    newArray = [csvArray[0]]
    for row in csvArray[1:]:
        for column in range(4,len(row)):
            newArray.append(row[:4]+[dates[column-4]]+[row[column]])

    with open(confirmed_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for row in newArray:
            spamwriter.writerow(row) 
    print(confirmed_file, "downloaded")

if __name__ == '__main__':
    crawl()