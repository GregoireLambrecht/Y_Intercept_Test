# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:23:26 2022

@author: Gregoire LAMBRECHT
"""
import pandas
import matplotlib.pyplot as plt 
from statistics import *

path = "data/data.csv"
dataCSV = pandas.read_csv(r"data/data.csv")
#print(dataCSV)

ticker = [int(x[0:-2]) for x in dataCSV['ticker']]
date = [x for x in dataCSV['date']]
last = [float(x) for x in dataCSV['last']]
volume = [float(x) for x in dataCSV['volume']]

dayBymonth=[31,28,31,30,31,30,31,31,30,31,30,31]

def countDays(dateOne,dateEnd):
    monthOne=int(dateOne[5:7])
    dayOne = int(dateOne[8:10])
    monthEnd=int(dateEnd[5:7])
    dayEnd = int(dateEnd[8:10])
    if(monthEnd==monthOne):
        return dayEnd - dayOne
    else:
        return dayBymonth[monthOne-1] - dayOne + dayEnd

day = [0]

for i in range(len(date)-1):
    day.append(day[-1] + countDays(date[i],date[i+1]))
    
    
def plotData():
    plt.figure()
    plt.plot(day,last)
    plt.title("last evolution by day")
    plt.xlabel("number of days")
    plt.ylabel("value of last")
    plt.legend()
    plt.show


    plt.figure()
    plt.plot(day,volume)
    plt.title("volume evolution by day")
    plt.xlabel("number of days")
    plt.ylabel("value of volume")
    plt.legend()
    plt.show


    

own=[ticker[0]]
invest=[-own[0]*last[0]]
real=[invest[0]+own[0]*last[0]]



def SimpleStrategy(dayConsider,propBuy,propSale,end,display=False):
    for i in range(dayConsider,end):
        lastSum=sum(last[i-dayConsider:i])
        volumeSum=sum(volume[i-dayConsider:i])
        
        lastMean=lastSum/dayConsider
        volumeMean=volumeSum/dayConsider
        
        if(last[i]>lastMean and volume[i]>volumeMean):
            buying = int(own[-1]*propBuy)
            invest.append(invest[-1]- buying*last[i])
            own.append(own[-1]+buying)
            real.append(invest[-1] + own[-1]*last[i])
            if display:
                print("buy")
            
        if(last[i]<lastMean and volume[i]>volumeMean):
            selling = int(own[-1]*propSale)
            invest.append(invest[-1] + selling*last[i])
            own.append(own[-1]-selling)
            real.append(invest[-1] + own[-1]*last[i])
            if display:
                print("sell")
        else :
            own.append(own[-1])
            invest.append(invest[-1])
            real.append(real[-1])
        if display:
            print(real[-1])
    return own,invest,real


#plotData()
SimpleStrategy(3,1/9,1/3,len(day),True)

#parameters example : dayConsider = 3, propBuy = 1/9, propSale = 1/3


            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    