import sys
from statistics import pvariance
from math import log10, sqrt
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

def main(args: list) -> int:
    items = dataLoad()
    #assume that it takes a normal distribution on a log scale by Central Limit Theorem
    #var(log10(product(x_i))) --> var(sum(log10(x_i)))
    #it is to adjust for it being a multiplier instead of additions
    for i, item in enumerate(items):
        items[i] = map(log10, item)
    
    var = 0.0827552697442 + sum(pvariance(item) for item in items) * 5 #Havium variance + (total variance * no. of loops)
    #0.0827552697442 is variance of Havium, obtained from https://www.desmos.com/calculator/lqd3nc4goo
    
    stdev = sqrt(var)
    print(f"Upgraders get within x{round(10**(3*stdev),2)} of the expected value 99.7% of the time.")

def main2(args: list) -> int:
    #plot cdf of log of all possible values
    items = dataLoad()
    for i, item in enumerate(items):
        items[i] = list(map(log10, item))
        mean = sum(items[i]) / len(items[i])
        for j in range(len(items[i])):
            items[i][j] -= mean
    test = list(map(sum, list(product(*items))))
    cdf(test)
    plt.show()
    return 0

def cdf(x, plot=True, *args, **kwargs):
    x, y = sorted(x), np.arange(len(x)) / len(x)
    return plt.plot(x, y, *args, **kwargs) if plot else (x, y)

def dataLoad():
    #item data
    items = []
    items.append([1,1,1,1,1,1,1,1,1.03**20]) #ench lib
    items.append([1.2**x for x in range(11,27)]) #astral
    items.append([105,110,115,120,125,130,135,140,145,150]) #meralin
    items.append([36,55,88,123]) #midas
    items.append([5,5.5,6,6.5,7,7.5]) #reaper's
    items.append([3,4,5]) #final faberge

    #enchLib = [1,1,1,1,1,1,1,1,1.03**20] #NOTE: enchanted library's rng multiplier is dependent on when ores reach it, as its a gradual upgrade over 10s
    return items

if __name__ == '__main__':
	sys.exit(main(sys.argv))
