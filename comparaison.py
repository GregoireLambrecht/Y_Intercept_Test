# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 00:24:47 2022

@author: grego
"""
from strategy import*
from BlackScholes import*

#------------------------------------------------------------------------------

#Strategie Comparaison 

#------------------------------------------------------------------------------

#Comparaison of the two strategies on the ticker ticker[5]
SimpleStrategy(5,100,3,1000,1/3,alldays[-1])
BlackScholes(5,100,100, 1000,100,alldays[-1],1/2)

#Comparaison on the two strategies on the ticker ticker[100]
SimpleStrategy(100,100,3,1000,1/3,alldays[-1])
BlackScholes(100,100,100, 1000,100,alldays[-1],1/2)

#Comparaison of the two startegies
_,_,realBS = PortFolioBS(10000, 100, alldays[-1], 100, 0.5)
_,_,realSS = PortFolioSS(10000,3,1/2,1000)

#Displays the last value of the strategy on each share
print("Black Sholes Strategy :")
print([realBS[tick][-1] for tick in range(len(ticker))])
print("Naive Strategy :")
print([realSS[tick][-1] for tick in range(len(ticker))])
print("Comparaison of the two startegies :")
print([realBS[tick][-1] - realSS[tick][-1] for tick in range(len(ticker))])