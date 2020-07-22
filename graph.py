import csv
import scipy.optimize as sci
import matplotlib.pyplot as plt
import datetime
import math
import numpy as np


def logistic(x, A, L, k, h):
    return L / (1 + A * (math.e ** (-k * (x - h))))

def fitModel(place):
    with open('usastates.csv') as temp:
        temp_data = csv.reader(temp)
        wuhan = {}
        for row in temp_data:
            if row[1] == 'US':
                if row[0] == place:
                    z = datetime.date(int(row[4][:4]), int(row[4][5:7]), int(row[4][8:]))
                    wuhan[z] = row[5]
                    #print('{}: {}'.format(z, row[5]))
        full = list(wuhan.keys())
        full.sort()
        if full:
            b = full[0]
            y_list = [int(wuhan[x]) for x in full]
            x_list = [(x - b).days for x in full]
            x_list = np.array(x_list)
            y_list = np.array(y_list)
            fit_params, pcov = sci.curve_fit(logistic, x_list, y_list,
                                            bounds=([-np.inf, y_list[-1], 0, 0], [np.inf, np.inf, 1, 50]), method='trf')
            print(fit_params)
            plt.scatter(x_list, y_list, label='wuhan')
            b = list(x_list)
            if fit_params[1] > y_list[-1]:
                for i in range(max(x_list) + 1, max(x_list) + 101):
                    b.append(i)
            #print (b)
        else:
            return []
        # x_list = np.array(b)
        # y_fit = logistic(x_list, *fit_params)
        # plt.plot(x_list, y_fit, label='fit', color='red')
        # plt.legend(loc='lower right')
        # plt.show()

placeSet = set()
with open('usastates.csv') as temp:
    place_data = csv.reader(temp)
    for row in place_data:
        placeSet.add(row[0])

for place in placeSet:
    fitModel(place)