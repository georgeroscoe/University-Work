#!/usr/bin/env python

"""
Implements an ARMA model on the tennis data.

"""


import os
import numpy as np
import pandas as pd
import pickle
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_pacf
from pandas.plotting import autocorrelation_plot

import matplotlib.pyplot as plt
bindir = 'bin2'

alph = 1.05
beta = 1.05*alph
wallet = 20000
Wallet = []
tobet = 50
odds_min = 10      # minimum number of odds available for a match
ts_min = 0*60*60000 # minimum time in minutes after which betting starts
verbose = 2

betwin = 0
betlos = 0
filecnt = 0

for f in os.listdir(bindir):

    # skip directories and files that start with _
    if '.' not in f or f.startswith("_"):
        continue

    filecnt += 1
    if verbose >= 1:
        print(f)

    filename = bindir + '/' + f
    Event = pickle.load(open(filename, 'rb'))
    names = Event['names']
    status = Event['status']
    lst = Event['odds']
    ts_play = Event['tsPlay'] # timestamp when match starts
    home = []
    away = []

    if len(Event['odds']) < odds_min:
        if verbose >= 2:
            print("   skipped because too few lines:", len(Event['odds']))
        continue

    if ts_play == 0:
        if verbose >= 2:
            print("    skipped because ts_play is 0")
        continue

    ts_first = lst[0][0]      # first available timestamp with odds

    pre_match = []

    for i in range(0, len(lst)):


        if (lst[i][0] - ts_play) < 0:
            #home.append(lst[i][1])
            #away.append(lst[i][2])
            pre_match.append(lst[i])



    """
    if ts_play-ts_first < 2*60*60000:
        print("   skipped because not enough pre-game betting:", ts_play-ts_first)
        continue
    """

    whichbet = 0
    linecnt = 0
    df = pd.DataFrame.from_records(pre_match)

    df.columns = ['Timestamp', 'Home Odds', 'Away Odds']
    indexed_df = df.set_index('Timestamp')
    #print(df.describe().transpose())
    #print(df.head())


    #log_scale = np.log(indexed_df)

    #model = ARIMA(indexed_df, order=(1, 2, 0))
    #model = ARIMA(indexed_df.values.reshape(-1).tolist(), order=(1,2,1))
    #results_ARIMA = model.fit(disp=-1)
    #plt.plot(indexed_df)
    #plt.plot(results_ARIMA.fittedvalues,color='red')
    #x = results_ARIMA.forecast(steps=10)
    #print(x[1])
    #df.plot(x='Timestamp')

    home_series = indexed_df['Home Odds']
    away_series = indexed_df['Away Odds']

    autocorrelation_plot(home_series)
    plt.show()
    plot_pacf(home_series)
    plt.show()
    #home_series.rolling(10).mean().plot()
    #home_series.plot()


    #acf = acf(home_series)
    #plt.plot(acf)

    #acf = acf(home_series)
    #acf.plot()
    print(type(home_series))
    break
    for line in lst:


        linecnt += 1
        ts = int(line[0])
        odd1 = float(line[1])
        odd2 = float(line[2])

        if not whichbet and ts - ts_first >= ts_min:
            if alph < odd1 <= beta:
                whichbet = 1
                if verbose >= 2:
                    print("   Bet on player 1 at", str(odd1), "(timestamp=" + str(ts) + ")")
                    print("   Pre-game:", bool(ts - ts_play < 0), "(time=" +str(ts-ts_play)+")")
                    print("   Nr of odds:", len(lst))
                betodd = odd1
                break
            if alph < odd2 <= beta:
                whichbet = 2
                if verbose >= 2:
                    print("   Bet on player 2 at", str(odd2), "(timestamp=" + str(ts) + ")")
                    print("   Pre-game:", bool(ts - ts_play < 0), "(time=" +str(ts-ts_play)+")")
                    print("   Nr of odds:", len(lst))
                betodd = odd2
                break

    if whichbet > 0 and status[whichbet-1] == "WINNER":
        betwin += 1
        wallet = wallet + tobet*(betodd-1)
        Wallet.append(wallet)
        if verbose >= 1:
            print("   WIN, wallet:", wallet)
    if whichbet > 0 and status[whichbet-1] == "LOSER":
        betlos += 1
        wallet -= tobet
        Wallet.append(wallet)
        if verbose >= 1:
            print("   LOSE, wallet:", wallet)
    if betlos > 0 and verbose >= 1:
        print("Total files:", filecnt, "| Total bets:", betwin+betlos, "| Win/lose ratio:", betwin/betlos)
    if wallet < 0:
        print("Ruined after parsing", filecnt, "files and playing", betwin+betlos, "bets.")
        print("Win bets:", betwin, ", Lose bets:", betlos, ", Win/lose ratio:", betwin/betlos)
        break

    if filecnt > 10000:
        break



plt.figure(figsize=(10, 7), dpi=80, facecolor='w', edgecolor='k')
plt.plot(Wallet)
plt.title(r'Wallet value after each bet with alpha = 1.05', fontsize=16)
plt.ylabel('Wallet value',fontsize=16)
plt.xlabel('Number of bets placed',fontsize=16)
plt.show()
