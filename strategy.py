# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:23:26 2022

@author: Gregoire LAMBRECHT
"""
import pandas
import matplotlib.pyplot as plt 
from statistics import *


#------------------------------------------------------------------------------

#Uploding data 

#------------------------------------------------------------------------------


path = "data/data.csv"
dataCSV = pandas.read_csv(r"data/data.csv")
#print(dataCSV)

ticker = [int(x[0:-2]) for x in dataCSV['ticker']]
date = [x for x in dataCSV['date']]
last = [float(x) for x in dataCSV['last']]
volume = [float(x) for x in dataCSV['volume']]

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
day = [0]


for i in range(len(date)-1):
    day.append(day[-1] + countDays(date[i],date[i+1]))
    
#day[i] is the number of days between the initial day and the date date[i]
    

#Just plotting the data
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


    
#own[i] : the number of shares held on date date[i] (at the day day[i])

#invest[i] : the money invested at the date date[i] (at the day day[i]). 
#If you invest at the day i+1 -> invest[i+1] = invest[i] - investment
#If you sell shares at the date i+1 -> invest[i+1] = invest[i] + recovered money
 
#real[i] : the money recovered plus the money invested plus the money in the market
#If real[i]<0 : you lost money 
#If real[i]>0 : you earn money
    
own=[ticker[0]]
invest=[-own[0]*last[0]]
real=[invest[0]+own[0]*last[0]]
#real[0] = 0

#Let's start with a really simple strategy.

#In this strategy every day we take into account the market values over the previous dayConsider days
#At the date i : 
#I. if the volume is lower than its average value of the previous dayConsider days, you don't do anything. 
#      --> We consider that Price moves made on low volume may be said to "lack conviction" and could be viewed as being less predictive of future returns.
#II. else : 
    #IF the price is lower than its average value of the previous dayConsider days, you sell your shares in a proportion of propSale
    #Else you buy new shares in a proportion of propBuy
    
#The goal is to find the better parameters dayConsider,propBuy,propSale, to maximize the values of real


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

#examples : dayConsider = 3, propBuy = 1/9, propSale = 1/3

SimpleStrategy(3,1/9,1/3,len(day),True)
print(real[-1])






            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    