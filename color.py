import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import unidecode
import matplotlib.pyplot as plt
import json

#ARGUMENTS ARE COUNTRY OR COUNTRY REGION
#RETURNS CURRENT STATE OF THE COUNTRY AS VALUE FROM 0 to 1. 1 IS GOOD AND 0 IS BAD
#Reads the csv file then puts the values into regionDict. This is sorted in the following way -> 
#regionDict["region, country"] = [(coordinates), (date, number of cases) <- for every date that is given]

printFile = 'color.json'

def run(file, typeOfDisplay, typeOfAnalysis):
    regionDict = {}

    with open(file) as f:
        tempDict = json.load(f)
    
    for place in tempDict:
        regionDict[place] = []
        for date in tempDict[place]:
            regionDict[place].append((date, tempDict[place][date]))
    
    retDict = {}
    for place in regionDict:
        retDict[place] = displayRegion(place, regionDict, typeOfAnalysis)

    if typeOfDisplay == "Normal":
        if typeOfAnalysis == "linear":
            for i in retDict:
                if retDict[i] == -10:
                    retDict[i] ="(0, 0, 0)"
                    continue
                if retDict[i] == -2.4:
                    color = 1
                    meaning = "No Cases"
                elif retDict[i] >= 1.5:
                    color = 0
                    meaning = "Exponential Increase"
                elif retDict[i] >= 1:
                    color = 1/6
                    meaning = "Decreasing Slope"
                elif retDict[i] >= .5:
                    color = 2/6
                    meaning = "Near 0, but increasing"
                elif retDict[i] >= 0:
                    color = 3/6
                    meaning = "Near 0, but decreasing"
                elif retDict[i] >= -.5:
                    color = 4/6
                    meaning = "Cases decreasing, but by less and less"
                elif retDict[i] >= -1:
                    color = 5/6
                    meaning = "Cases decreasing by more and more"
                color = str(numToColor(color))
                retDict[i] = color.replace(" ", "")
        else:
            for i in retDict:
                color = str(numToColor(float(retDict[i])))
                retDict[i] = color.replace(" ", "")
    
    elif typeOfDisplay == "Relative":
        newArray = []
        for i in retDict:
            newArray.append((retDict[i], i))
        newArray.sort()
        if typeOfAnalysis != "linear":
            newArray = newArray[::-1]
        sortedArray = []
        for i in range(1,7):
            sortedArray.append(newArray[ int(len(newArray)*(i-1)/6) :int(len(newArray)*i/6)+1])

        for i in range(len(sortedArray)):
            for place in sortedArray[i]:
                color = str(numToColor(1-((i+1)/6)))
                retDict[place[1]] = color.replace(" ", "")

    with open(printFile, 'w') as f: json.dump(retDict, f, ensure_ascii=False)

def displayRegion(region, regionDict, t):
    data = sorted(regionDict[region][::-1])
    temp = {}
    for i in data:
        if i[0] not in temp:
            temp[i[0]] = 0
        temp[i[0]] += i[1]
    
    data = []
    for i in temp:
        data.append((i, temp[i]))
        
    x = [i for i in range(len(data))][:-1]
    y = [float(i[1]) for i in data][:-1]

    changeY = []
    for i in range(1,len(y)):
        changeY.append(y[i]-y[i-1])

    daysBack = 10
    if x and y and changeY:
        if t == "linear":
            temp = linearFit(x,y,changeY,daysBack)
        else:
            temp = reopenState(y,daysBack)
    else:
        return (-10)
    return temp


def origional(x, y, changeY):
    color = 0
    meaning = ""
    if x[-1] == 0:
        color = 1
        meaning = "No Cases"
    elif sum(changeY[-3:])/3 < 0:
        color = .75
        meaning = "Decreasing"
    elif (sum(changeY[-3:])/3) < .01*x[-1]:
        color = .5
        meaning = "Plateau"
    elif sum(changeY[-3:])<sum(changeY[-6:-3]):
        color = .25
        meaning = "Decreasing Slope"
    else:
        color = 0
        meaning = "Increasing Slope"

    color = str(numToColor(color))

    return (color.replace(" ", ""), meaning)

def linearFit(x,y,changeY, daysBack):
    newX = x[-daysBack:]
    newY = y[-daysBack:]
    
    newChangeY = changeY[-daysBack:]

    if len(newChangeY) != len(newX):
        newX = newX[:-len(newChangeY)]
        newY = newY[:-len(newChangeY)]

    avg = (sum([x for x in newChangeY]))
    
    if newY[-1] == 0:
        changeNum = -3
    elif abs(avg) < .03*y[-1]:
        changeNum = 0
    elif avg > 0:
        # if avg > .07*y[-1]:
        #     changeNum = 1.25
        # else:
        changeNum = 1
    else:
        changeNum = -1

    if sum(newY) and sum(newX):
        b, a = best_fit(newX, newChangeY)
    else:
        return -10
    
    if a == 0:
        temp = .5
    elif a > 0:
        temp = .5 + a/9000000000
    elif a < 0:
        temp = -a/9000000000
    
    colorNum = temp
    if changeNum == -3:
        colorNum = -2.4
    else:
        colorNum += changeNum

    return colorNum
    # plt.clf()
    # plt.scatter(newX, newChangeY)
    # yfit = [a + b * xi for xi in newX]
    # plt.plot(newX, yfit)

def reopenState(y,daysBack):
    # Specific example
    tmSqnc = y[-daysBack:]
    deltas = [n-tmSqnc[j] for j,n in enumerate(tmSqnc[1:])]
    # deltas = [23, 45, 45, 17, 12, -7, -9, 2, 0, -6]
    zo = "".join([str(0+(n>0)) for n in deltas])
    # zo = zero/one string
    last = 1+zo.rfind('1')            # 1+ => better normalization
    pct = zo.count('1')
    badness= pct*last / len(zo)**2
    # negative = not not [x for x in deltas if x < 0]
    # if badness != 1 or negative:
    #     print(badness)
    #     print (deltas)
    return 1-badness

    # Comparison for a range of 0...2**bits
    bits = daysBack
    lstZOs = [format(n,"0{}b".format(bits)) for n in range(2**bits)]  # Generated every bit string in range

    dctBad = {zo:(1+zo.rfind('1'))*zo.count('1') for zo in lstZOs}
    showBad= {n:{zo for zo in dctBad if dctBad[zo]==n} for n in sorted(dctBad.values())}
    for n in showBad: print(n/bits**2,showBad[n])
    
    # The division normalizes from 0 to 1

def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    return a, b

#Takes number 0 (bad) to 1 (good) and returns tuple of color
def numToColor(num):
    red = 255
    green = 0
    blue = 0

    if num <= .5:
        green = int(255 * (num/.5))
    else:
        green = 255
        red = int (255 - (255 * (num-.5)/.5))
    
    return ((red,green,blue))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

#ACCEPTS COUNTRY OR COUNTRY REGION
#if len(sys.argv) == 3:
#    print (displayRegion(sys.argv[2] + ", " + sys.argv[1], regionDict))
#elif len(sys.argv) == 2:
#    print (displayRegion(sys.argv[1], regionDict))

#Uncomment to show graph
#plt.show()
def crawl():
    run("global.json", "Relative", "linear")

if __name__ == '__main__':
    crawl()