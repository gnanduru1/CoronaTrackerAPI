import os
from shutil import copyfile

def moveFiles():
    for i in ['color.json', 'countries_110.json', 'currency_country.json', 'curr_code_to_name.json', 'custom.json', 'custom2.json', 'exchange_rate_global.json', 'global.json', 'historic_stocks.json', 'status.json', 'stocks.json', 'stock_countries.json']:
        copyfile(i, 'data/'+i)

if __name__ == '__main__':
    moveFiles()