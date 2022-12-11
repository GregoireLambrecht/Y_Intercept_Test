# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:07:04 2022

@author: grego
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:23:26 2022

@author: Gregoire LAMBRECHT
"""
import pandas
import matplotlib.pyplot as plt 
from statistics import *
from math import *

#------------------------------------------------------------------------------

#Uploding data 

#------------------------------------------------------------------------------


path = "data/data.csv"
dataCSV = pandas.read_csv(r"data/data.csv")
#print(dataCSV)
tickerCSV = [x[0:-3] for x in dataCSV['ticker']]
dateCSV = [x for x in dataCSV['date']]
lastCSV = [float(x) for x in dataCSV['last']]
volumeCSV = [float(x) for x in dataCSV['volume']]

ticker=[]
DATE = []
LAST = []
VOLUME = []

tick = tickerCSV[0]
ticker.append(tick)
d =[]
l = []
v = []

for i in range(len(tickerCSV)):
    if(tickerCSV[i] == tick):
        d.append(dateCSV[i])
        l.append(lastCSV[i])
        v.append(volumeCSV[i])
    else:
        DATE.append(d)
        LAST.append(l)
        VOLUME.append(v)
        tick = tickerCSV[i]
        ticker.append(tick)
        d =[]
        l = []
        v = []

DATE.append(d)
LAST.append(l)
VOLUME.append(v)
        
#Number of days in the ith month 
dayBymonth=[31,28,31,30,31,30,31,31,30,31,30,31]

#Return the number of days between two days separated for less than a month
def countDays(dateOne,dateEnd):
    monthOne=int(dateOne[5:7])
    dayOne = int(dateOne[8:10])
    monthEnd=int(dateEnd[5:7])
    dayEnd = int(dateEnd[8:10])
    if(monthEnd==monthOne):
        return dayEnd - dayOne
    else:
        return dayBymonth[monthOne-1] - dayOne + dayEnd

#0 -> correspond do the first date 2013-01-04 : it is the initial day

day = []

for i in range(len(ticker)):
    d=[countDays(DATE[0][0],DATE[i][0])]
    for j in range(len(DATE[i])-1):
        d.append(d[-1] + countDays(DATE[i][j],DATE[i][j+1]))
    day.append(d)
    
#day[i] is the number of days between the initial day and the date date[i]

endDay = max([max(day[tick]) for tick in range(len(ticker))])

last = []
volume = []

for tick in range(len(ticker)):
    dOne = day[tick][0]
    l=[]
    v=[]
    j=0
    while(j<=dOne):
        l.append(LAST[tick][0])
        v.append(VOLUME[tick][0])
        j+=1
    k=1
    for k in range(1,len(day[tick])):
        while(j<=day[tick][k] and k<len(day[tick])):
            l.append(LAST[tick][k])
            v.append(VOLUME[tick][k])
            j+=1
    while(j<=endDay):
        l.append(LAST[tick][-1])
        v.append(VOLUME[tick][-1])
        j+=1
    last.append(l)
    volume.append(v)
    
alldays = [i for i in range(endDay+1)]
    

#Just plotting the data
def plotData(i):

    plt.figure()
    plt.plot(alldays,last[i]) 
    plt.title("Price evolution of the ticker " + ticker[i])
    plt.xlabel("Number of days")
    plt.ylabel("Price")
    plt.show

    plt.figure()
    plt.plot(alldays,volume[i])
    plt.title("volume evolution of the ticker " + ticker[i])
    plt.xlabel("Number of days")
    plt.ylabel("Volume")
    plt.show
    
        
    