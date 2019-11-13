#!/usr/bin/env python

"""
Loads PL Season Data, and contains the Strategy 1 function.
"""
import csv
import matplotlib.pyplot as plt
import numpy

pl1819_file = open('PL1819Data.csv')
reader = csv.reader(pl1819_file)
pl1819 = list(reader)



def Strategy1(alph, beta, data):
    wallet = 20000
    tobet = 0.05*wallet
    Wallet = [wallet]

    data_length = len(data)

    no_of_bets = 0
    for i in range(1, data_length):

        sum_home_odds = float(0.0)
        sum_away_odds = float(0.0)

        for j in range(0, 16, 3):
            sum_home_odds += float(data[i][23+j])
        for j in range(0, 16, 3):
            sum_away_odds += float(data[i][25+j])

        av_home_odds = sum_home_odds / 6
        av_away_odds = sum_away_odds / 6

        av_home_odds = float(data[i][59])
        av_away_odds = float(data[i][61])

        #home_odds = float(data[i][23])
        #away_odds = float(data[i][25])
        if alph <= av_home_odds <= beta:
            no_of_bets += 1
            if data[i][6] == 'H':

                wallet = wallet + (tobet*(av_home_odds-1.0))
                tobet = 0.05*wallet
                Wallet.append(wallet)
                #print('Success!')
            else:
                wallet = wallet - tobet
                tobet = 0.05*wallet
                Wallet.append(wallet)
                #print('Failure')
        if alph <= av_away_odds < beta:
            no_of_bets += 1
            #print('Match number ', i)
            if data[i][6] == 'A':

                wallet = wallet + (tobet*(av_away_odds-1.0))
                tobet = 0.05*wallet
                Wallet.append(wallet)
                #print('Success!')
            else:
                wallet = wallet - tobet
                tobet = 0.05*wallet
                Wallet.append(wallet)
                #print('Failure')

    plt.figure(figsize=(10, 7), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(Wallet)
    plt.ylabel('Wallet value')
    plt.xlabel('Number of bets placed')
    plt.title('Wallet value after each bet with alpha = 1.25')
    plt.show()

    #print(Wallet[-1])
    return wallet

if __name__ == "__main__":
    Strategy1(1.25,1.3125,pl1819)
