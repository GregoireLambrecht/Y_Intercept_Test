# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:23:26 2022

@author: Gregoire LAMBRECHT
"""
import pandas
import matplotlib.pyplot as plt 
from statistics import *

from dataProcessing import *
    
#real[0] = 0

#Let's start with a really simple strategy.

#In this strategy every day we take into account the market values over the previous dayConsider days
#At the date i : 
#I. if the volume is lower than its average value of the previous dayConsider days,  don't do anything. 
#      --> We consider that price moves made on low volume may be said to "lack conviction" and are viewed as being less predictive of future returns.
#II. else : 
    #IF the price is lower than its average value of the previous dayConsider days, you sell your shares in a proportion of propSale
    #Else you buy new shares in a proportion of propBuy
    
#The goal is to find the better parameters dayConsider,propBuy,propSale, to maximize the values of real


def SimpleStrategy(tick,x,dayConsider,buy,propSale,end):
    shares=[x]
    invest=[-shares[0]*last[tick][0]]
    real=[invest[0]+shares[0]*last[tick][0]]
    for i in range(dayConsider,end):
        lastSum=sum(last[tick][i-dayConsider:i])
        volumeSum=sum(volume[tick][i-dayConsider:i])
        
        lastMean=lastSum/(dayConsider-1)
        volumeMean=volumeSum/(dayConsider-1)
        
        if(last[tick][i]>lastMean and volume[tick][i]>volumeMean):
            buying = buy/last[tick][i]
            invest.append(invest[-1]- buying*last[tick][i])
            shares.append(shares[-1]+buying)
            real.append(invest[-1] + shares[-1]*last[tick][i])

        elif (last[tick][i]<lastMean and volume[tick][i]>volumeMean):
            selling = int(shares[-1]*propSale)
            invest.append(invest[-1] + selling*last[tick][i])
            shares.append(shares[-1]-selling)
            real.append(invest[-1] + shares[-1]*last[tick][i])

        else :
            shares.append(shares[-1])
            invest.append(invest[-1])
            real.append(real[-1])

    plotData(tick)
    plt.figure()
    plt.plot([i for i in range(len(real))],real)
    plt.xlabel("days")
    plt.ylabel("Money")
    plt.title("Naive Strategy on the ticker "+ticker[tick])
    plt.show
    return shares,invest,real

#examples : dayConsider = 3, propBuy = 1/9, propSale = 1/3

#shares,invest,real = SimpleStrategy(5,100,3,1000,1/3,alldays[-1])

def PortFolioSS(initInvest,dayConsider,propSale,end):
    ntick =len(ticker)
    buy = initInvest/ntick
    shares=[[buy/last[tick][0]] for tick in range(ntick)]
    invest=[[-shares[tick][0]*last[tick][0]] for tick in range(ntick)]
    real=[[invest[tick][0]+shares[tick][0]*last[tick][0]] for tick in range(ntick)]
    
    REAL = [0]
    
    
    for i in range(dayConsider,end):
        for tick in range(ntick):
            lastSum=sum(last[tick][i-dayConsider:i])
            volumeSum=sum(volume[tick][i-dayConsider:i])
            
            lastMean=lastSum/(dayConsider-1)
            volumeMean=volumeSum/(dayConsider-1)
            
            if(last[tick][i]>lastMean and volume[tick][i]>volumeMean):
                buying = buy/last[tick][i]
                invest[tick].append(invest[tick][-1]- buying*last[tick][i])
                shares[tick].append(shares[tick][-1]+buying)
                real[tick].append(invest[tick][-1] + shares[tick][-1]*last[tick][i])

            elif (last[tick][i]<lastMean and volume[tick][i]>volumeMean):
                selling = int(shares[tick][-1]*propSale)
                invest[tick].append(invest[tick][-1] + selling*last[tick][i])
                shares[tick].append(shares[tick][-1]-selling)
                real[tick].append(invest[tick][-1] + shares[tick][-1]*last[tick][i])


            else :
                shares[tick].append(shares[tick][-1])
                invest[tick].append(invest[tick][-1])
                real[tick].append(real[tick][-1])
        REAL.append(REAL[-1] + sum([real[tick][-1] for tick in range(ntick)]))

    plt.figure()
    plt.plot([i for i in range(len(REAL))],REAL)
    plt.xlabel("days")
    plt.ylabel("Money")
    plt.title("Naive Strategy on the total Stock ")
    plt.show
    return shares,invest,real

#shares,invest,real = PortFolioSS(10000,3,1/2,1000)






            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    