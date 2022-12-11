from dataProcessing import *

#plotData(0)
    
#------------------------------------------------------------------------------


#In this file we present a strategy using Black Scholes financial coverage


#SHORT EXPLANATION OF THE MODEL 

#We suppose that the price of the share follows a Black and Scholes eqution 

#Such that the price at time t is S_{t} = s0*exp((MU - (SIGMA^2)/2)*t + SIGMA* Wt)
#Where (Wt) is a Brownian motion

#We know that EXPECTED_VALUE(S_t) = E(St) = s0*exp(MU*t)
#So, if MU >0, it could be relevant to buy shares because we expect that the price will increase in future days

#Then we would like to know the MU. 

#Since log(S_{t2}) - log(S_{t1}) =(in law) N(mu = (MU - 1/2 * SIGMA^2)(t2-t1), sigma^2 = SIGMA^2(t2 - t1)) 
#We could predict the value of mu and sigma by using estimators (with the law of large numbers), and the MU and SIGMA

#We calculate an estimate of mu with the empirical mean and an estimate of sigma with the emperical variance
#Then we obtain MU and SIGMA

#We decide to take action every @mooveTime days

#If the value of MU determined so far is non negative we buy shares (for @buy dollars)

#If the value is negative we sell shares (in a proportion of @propSell)


#-----------------------------------------------------------------------------


#x : number of shares we buy at the beginning
#tick : model for the share ticker[tick]
#begin : We don't take any moove before the time begin, we observe the market to obtain a first estimate of SIGMA and MU
#end : last date


def BlackScholes(tick,x,begin, end,mooveTime,buy,propSell):
    #Average value of t2-t1
    shares = [x]
    real = [0]
    invest = [x*last[tick][0]]
    Dl = [log(last[tick][i+1]/last[tick][i]) for i in range(begin)]
    mu = [mean(Dl)]
    sigma = [mean([(Dl[j]-mu[-1])*(Dl[j]-mu[-1]) for j in range(begin)])]
    MU = [mu[-1]/sigma[-1]]
    SIGMA = [sqrt(sigma[-1])]
    
    for i in range(begin,end-1):
        Dl.append(log(last[tick][i+1]/last[tick][i]))
        m = (mu[-1]*i + Dl[-1])/(i+1)
        #m = mean(Dl)
        mu.append(m)
        sigma.append((sigma[-1]*len(sigma) + (Dl[-1]-mu[-1])*(Dl[-1]-mu[-1]))/(len(sigma)+1))
        #sigma.append(mean([(Dl[j]-m)*(Dl[j]-m) for j in range(i+1)]))
        MU.append(mu[-1]+sigma[-1]/2)
        SIGMA.append(sqrt(sigma[-1]))
        if(i%mooveTime==0):
            if (MU[-1]>0): 
                #buying =  shares[-1]*positivePart(1-SIGMA[-1])
                #buying =  shares[-1]/4
                buying = buy/last[tick][i+1]
                shares.append(shares[-1] + buying )
                invest.append(invest[-1] - buying*last[tick][i+1])
                real.append(invest[-1] + shares[-1]*last[tick][i+1])
            elif (MU[-1]<0):
                #selling =  shares[-1]*positivePart(1-SIGMA[-1])
                selling =  shares[-1]*propSell
                shares.append(shares[-1] - selling )
                invest.append(invest[-1] + selling*last[tick][i+1])
                real.append(invest[-1] + shares[-1]*last[tick][i+1])  
        else :
            invest.append(invest[-1])
            shares.append(shares[-1])
            real.append(invest[-1] + shares[-1]*last[tick][i+1])
    plotData(tick)
    plt.figure()
    plt.plot([i for i in range(len(real))],real)
    plt.xlabel("Days")
    plt.ylabel("Earned money")
    plt.title("Strategy on the ticker " + ticker[tick])
    plt.show
    plt.figure()
    plt.figure()
    plt.plot([i for i in range(len(real))],shares)
    plt.xlabel("Days")
    plt.ylabel("Shares")
    plt.title("BS Strategy_Shares " + ticker[tick])
    plt.show
    
    
    return shares,invest,real

#share, invest, Real = BlackScholes(5,100,100, 1000,100,1000,1/2)



def PortFolioBS(initInvest,begin,end,mooveTime,propSell):
    #Average value of t2-t1
    ntick = len(ticker)
    buy = initInvest/ntick
    
    shares = [[buy/last[tick][0]] for tick in range(ntick)]
    real = [[0] for tick in range(ntick)]
    invest = [[-buy] for tick in range(ntick)]
    REAL = [0]
    
    Dl = [[log(last[tick][i+1]/last[tick][i]) for i in range(begin)] for tick in range(ntick)]
    mu = [[mean(Dl[tick])] for tick in range(ntick)]
    sigma = [[mean([(Dl[tick][j]-mu[tick][-1])*(Dl[tick][j]-mu[tick][-1]) for j in range(begin)])] for tick in range(ntick)]
    
    MU = [[mu[tick][-1] + sigma[tick][-1]/2] for tick in range(ntick)]
    SIGMA = [[sqrt(sigma[tick][-1])] for tick in range(ntick)]
    
    for i in range(begin,end-1):
        for tick in range(ntick):
            Dl[tick].append(log(last[tick][i+1]/last[tick][i]))
            m = (mu[tick][-1]*i + Dl[tick][-1])/(i+1)
            #m = mean(Dl)
            mu[tick].append(m)
            sigma[tick].append((sigma[tick][-1]*len(sigma) + (Dl[tick][-1]-mu[tick][-1])*(Dl[tick][-1]-mu[tick][-1]))/(len(sigma[tick])+1))
            #sigma.append(mean([(Dl[j]-m)*(Dl[j]-m) for j in range(i+1)]))
            MU[tick].append(mu[tick][-1] + sigma[tick][-1]/2)
            SIGMA[tick].append(sqrt(sigma[tick][-1]))
            
            if(i%mooveTime==0):
                if MU[tick][-1]>0: 
                    #buying =  shares[-1]*positivePart(1-SIGMA[-1])
                    #buying =  shares[-1]/4
                    buying = buy/last[tick][i+1]
                    shares[tick].append(shares[tick][-1] + buying )
                    invest[tick].append(invest[tick][-1] - buying*last[tick][i+1])
                    real[tick].append(invest[tick][-1] + shares[tick][-1]*last[tick][i+1])
                elif MU[tick][-1]<0:
                    #selling =  shares[-1]*positivePart(1-SIGMA[-1])
                    selling =  shares[tick][-1]*propSell
                    shares[tick].append(shares[tick][-1] - selling )
                    invest[tick].append(invest[tick][-1] + selling*last[tick][i+1])
                    real[tick].append(invest[tick][-1] + shares[tick][-1]*last[tick][i+1])  
            else :
                invest[tick].append(invest[tick][-1])
                shares[tick].append(shares[tick][-1])
                real[tick].append(invest[tick][-1] + shares[tick][-1]*last[tick][i+1])
        REAL.append(REAL[-1] + sum([real[tick][-1] for tick in range(ntick)]))
    plt.figure()
    plt.plot([i for i in range(len(REAL))],REAL)
    plt.xlabel("Days")
    plt.ylabel("Money")
    plt.title("BS Strategy on the total Stock ")
    plt.show
    return shares,invest,real
          
#shares,invest,real = PortFolioBS(10000, 100, alldays[-1], 100, 0.5)
          
          
         

