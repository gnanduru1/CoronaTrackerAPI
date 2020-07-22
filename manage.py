from threading import Timer
import who, europe, asia, usacases, econ, stocks, color, process
import os

def collect():    
    who.crawl() # Make sure WHO runs first, because we will be overwriting WHO data with localized sources
    europe.crawl()       
    asia.crawl()
    usacases.crawl()    
    econ.crawl()
    stocks.crawl()
    color.crawl()

def load():
    process.toJSON()
    process.init()
    process.status()
    process.bigCountries()
    process.convert()

def moveFiles():
    for i in [j for j in os.listdir('.') if '.json' in j or '.csv' in j]:
        try:
            os.replace(i, "../react-app/src/data/"+i)
        except:
            os.mknod(i, "../react-app/src/data/"+i)
            os.replace(i, "../react-app/src/data/"+i)

def cycle():
    collect()
    load()
    moveFiles()
    exit()
    timer = Timer(3600*24, cycle)
    timer.start()

cycle()