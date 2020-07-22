from flask import Flask, render_template, url_for
from flask_cors import CORS
import os
import process, usacases, europe, who, asia, econ, stocks, color
import io
# Info descriptions
general_info = "PyCrawler Homepage"
endpoint_info = {
    "/regions": "to list available regions in region-country format",
    "/history/{region-country}/{date or all}": "to get global COVID-19 data for a single region on a certain day.",
    "/currency/{date or all}": "get currency tables for date",
    "/stocks/{date or all}": "national stock index for date",
    "/refresh": "rerun crawler",
    "/asiacases": "list all the asia cases and its dates",
    "/usacases": "list all the cases in the us by state and its dates",
    "/europecases": "list all the europe cases and its dates",
    "/globalcases": "list all the cases collected globally and its dates",
    "/color": "lists colors for every region"
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h1>you cannot say pop and forget the smoke</h1>"

@app.route('/regions')
def regions():
    return str(process.keys())

@app.route('/history')
def history():
    with open('global2.json') as f:
        return f.read()

############## TEMPORARY #######################
@app.route('/big_countries_names')
def big_countries_names():
    with open('big_countries.json') as f:
        return f.read()

@app.route('/countries_names')
def countries_names():
    with open('countries.json') as f:
        return f.read()

@app.route('/currency_info')
def currency_info():
    with open('currency_country.json') as f:
        return f.read()

@app.route('/currency_code_to_name')
def currency_code_to_name():
    with io.open('curr_code_to_name.json', mode="r", encoding="utf-8") as f:
        return f.read()

@app.route('/country_to_stocks')
def country_to_stocks():
    with open('stock_countries.json') as f:
        return f.read()

@app.route('/big_countries/<country>')
def big_countries(country):
    with open('./big_countries/' + country + '.json') as f:
        return f.read()

@app.route('/countries/<country>')
def countries(country):
    try:
        with open('countries2/' + country + '.json') as f:
            return f.read()
    except:
        print(country,'defaulted')
        with open('countries/' + country + '.json') as f:
            return f.read()
        

@app.route('/custom') # experimental endpoint, will replace /countries/ once configured
def custom():
    with open('custom.json') as f:
        return f.read()

@app.route('/custom2') # experimental endpoint, will replace /big_countries/ once configured
def custom2():
    with open('custom2.json') as f:
        return f.read()

@app.route('/default')
def default_data_temp():
    with io.open('countries_110.json', mode="r", encoding="utf-8") as f:
        return f.read()
################################################

@app.route('/refresh')
def refresh():    
    who.crawl() # Make sure WHO runs first, because we will be overwriting WHO data with localized sources

    europe.crawl()       
    asia.crawl()
    usacases.crawl()    
    econ.crawl()
    stocks.crawl()
    process.convert() # do the convertDict name replacements immediately after downloads finish
    
    process.init()    
    process.bigCountries() # once bigdict is made, get all the countries where regional data is available
    process.status()
    color.crawl() # dependent on status.csv
    process.toJSON() # after everything is done convert to json
    process.customConfig() # configure custom.json countries-in-one endpoint
    return "Success"

@app.route('/status')
def status():
    with open('status.json') as f:
        return f.read()

@app.route('/currency')
def currency():
    with open("exchange_rate_global.json") as f:
        return f.read()

@app.route('/stocks')
def nsi():
    with open('historic_stocks.json') as f:
        return f.read()

@app.route('/color')
def colorCode():
    with open('color.json') as f:
        return f.read()

if __name__ == "__main__":
    app.run()