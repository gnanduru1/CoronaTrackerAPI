import requests, json
import lxml.html as lh
from datetime import date
from os import path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

indicies = ['The Global Dow', 'Dow Jones', 'NASDAQ 100', 'NASDAQ Composite', 'NYSE International 100', 'NYSE US 100', 
    'Russell 2000', 'S&P 500', 'IPC', 'S&P/TSX', 'VIX', 'U.S. Dollar Index', 'DAX', 'DivDAX', 'MDAX', 'TecDAX', 
    'AEX', 'CAC 40', 'FTSE 100', 'IBEX 35', 'OMXS30', 'SMI', 'BOVESPA', 'BSX', 'IGPA', 'IBC', 'BVQ', 
    'BET', 'BUX', 'PX', 'RTS', 'RTX USD', 'SAX', 'EGX30', 'KSE 100', 'NSE 20', 'Australia All Ordinaries', 
    'Hang Seng', 'KOSPI', 'NIKKEI 225', 'SENSEX', 'Shanghai Composite']

toUse = ['dow_jones_global_dow', 'Dow Jones', 'NASDAQ 100', 'NASDAQ Composite', 'NYSE International 100', 'NYSE US 100', 
    'Russell 2000', 'S&P 500', 'IPC', 'S&P TSX Composite Index', 'VIX', 'US-Dollar-Index', 'DAX', 'DivDAX', 'MDAX', 'TecDAX', 
    'AEX', 'CAC 40', 'FTSE 100', 'IBEX 35', 'OMX', 'SMI', 'BOVESPA', 'BSX', 'IGPA', 'IBC', 'BVQ', 
    'BET', 'BUX', 'PX', 'RTS', 'RTX', 'SAX', 'EGX30', 'KSE 100', 'NSE', 'asx', 
    'Hang Seng', 'KOSPI', 'NIKKEI 225', 'SENSEX', 'Shanghai Composite']

daniel = 'C:/Users/Daniel/Desktop/chromedriver.exe'
ganesh = r"C:\Users\Ganes\Downloads\chromedriver"
stock_file = 'historic_stocks.json'

driver = webdriver.Chrome(ganesh)

count = 0

try:
    with open(stock_file, 'r') as f:
            dct = json.load(f)
except:
    pass

try:
    for index in toUse:
        temp = index.lower().replace(" ","_")

        today = str(date.today())
        year, month, day = today[:4], today[5:7], today[-2:]
        d = "{}.{}.{}".format(day, month, year)

        stock_url = "https://markets.businessinsider.com/index/historical-prices/{}/1.1.2020_{}".format(temp, d)
        print (temp)

        driver.get(stock_url)

        python_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="request-historic-price"]')))
        python_button.click()
        time.sleep(1)

        data = []
        for table in driver.find_elements_by_xpath('//*[@id="historic-price-list"]//tr')[1:]:
            data.append([indicies[count]] + [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")])
        
        for d in data:
            month = d[1][:d[1].index('/')]
            if len(month) == 1: month = '0' + month
            temp = d[1][d[1].index('/')+1:]
            day = temp[:temp.index('/')] 
            if len(day) == 1: day = '0' + day
            d[1] = d[1][-4:] + '-' + month + '-' + day
            
            if d[0] not in dct: dct[d[0]] = {d[1]:float(d[2])}
            else: dct[d[0]][d[1]] = float(d[2])
        count += 1
except Exception as err:
    print(err)
finally:
    with open(stock_file, 'w') as f:
        json.dump(dct, f)
    driver.quit()