import json, time
import numpy as np
import pandas as pd
from math import factorial
import matplotlib.pyplot as plt
#ARGUMENTS ARE COUNTRY OR COUNTRY REGION
#RETURNS CURRENT STATE OF THE COUNTRY AS VALUE FROM 0 to 1. 1 IS GOOD AND 0 IS BAD
#Reads the csv file then puts the values into regionDict. This is sorted in the following way -> 
#regionDict["region, country"] = [(coordinates), (date, number of cases) <- for every date that is given]

RED = '#ff0000'
R_ORANGE = '#ff5400'
ORANGE = '#ffb700'
YELLOW = '#ffff00'
Y_GREEN = '#c8ff00'
GREEN = '#00ff00'
GREY = "#808080"

input_file = 'data/all.json'
output_file = 'data/color2.json'

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

def run():
    colorDict = {}
    with open(input_file) as f:
        df = pd.read_json(f)
        cnt = 0
        for name in set(df.columns):
            cnt += 1
            target = df[name].sort_index().dropna()
            dates = np.asarray([(i-target.index[0]).days for i in target.index])
            dates = dates[::len(dates)//40 or 1]
            cases = target.values[::len(target.values)//40 or 1]
            if cases[-1] < 10: 
                colorDict[name] = GREEN
                continue
            if len(cases)<5: 
                colorDict[name] = GREY
                continue     

            # Adds the last three values for the 1st/2nd derivatives of the cases vs. time graph
            # Examine both of these to determine the behavior of cases vs. time graph           
            d1 = savitzky_golay(cases, 51, 3, deriv=1)
            d2 = savitzky_golay(cases, 51, 3, deriv=2)
            slope = sum(d1[-3:])
            concavity = sum(d2[-3:])

            if slope < 0:
                colorDict[name] = Y_GREEN
            elif slope < 20:
                colorDict[name] = YELLOW
            elif slope > 0 and concavity < 0:
                colorDict[name] = ORANGE
            elif slope > 0 and abs(concavity) < 1:
                colorDict[name] = R_ORANGE
            elif slope > 0 and concavity > 0:
                colorDict[name] = RED

            # GRAPHICAL DISPLAY
            # WILL KEEP SHOWING DATA + CORRESPONDING COLOR UNTIL CTRL+C IS PRESSED
            # CLOSE PLOT WINDOW TO SHOW NEXT REGION
            
            # fig, axs = plt.subplots(1,3)
            # axs[0].scatter(dates, cases, s=2, c=colorDict[name])
            # axs[1].scatter(dates, d1, s=2,c=colorDict[name])
            # axs[2].scatter(dates, d2, s=2,c=colorDict[name])
            # fig.canvas.set_window_title(name)
            # plt.show()
            # plt.close()
            
            print('{}/{}'.format(cnt, len(df.columns)), end='\r')
    
    with open(output_file, 'w') as f: json.dump(colorDict, f, ensure_ascii=False)

if __name__ == '__main__':
    run()