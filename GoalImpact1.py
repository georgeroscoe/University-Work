#!/usr/bin/env python

"""
Grab goalimpact data and compare to historic oddss data.
"""

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
import numpy as np
from scipy.optimize import brute


chship1920file = open('CHSHIP1920DATA.csv')
reader_ch = csv.reader(chship1920file)
data_ch= list(reader_ch)

gifile = open('GoalImpactData.csv')
reader_gi = csv.reader(gifile)
data_gi = list(reader_gi)


bigdatafile = open('BigData.csv')
reader_big = csv.reader(bigdatafile)
data_big = list(reader_big)



teams1819 = ['Aston Villa',
             'Barnsley',
             'Birmingham',
             'Blackburn',
             'Brentford',
             'Fulham',
             'Huddersfield',
             'Hull',
             'Luton',
             'Millwall',
             'Norwich',
             'Forest',
             'Preston',
             'QPR',
             'Reading',
             'Sheffield Un',
             'Sheffield We',
             'Stoke',
             'Swansea',
             'Wigan']

teams = ['Barnsley',
         'Birmingham',
         'Blackburn',
         'Brentford',
         'Bristol',
         'Cardiff',
         'Charlton',
         'Fulham',
         'Huddersfield',
         'Hull',
         'Leeds',
         'Luton',
         'Middles',
         'Millwall',
         'Forest',
         'Fulham',
         'Preston',
         'QPR',
         'Reading',
         'Sheffield We',
         'Stoke',
         'Swansea',
         'West Brom',
         'Wigan']


full_team_list = ['Barnsley',
                  'Birmingham',
                  'Blackburn',
                  'Brentford',
                  'Bristol',
                  'Cardiff',
                  'Charlton',
                  'Fulham',
                  'Huddersfield',
                  'Hull',
                  'Leeds',
                  'Luton',
                  'Middles',
                  'Millwall',
                  'Forest',
                  'Fulham',
                  'Preston',
                  'QPR',
                  'Reading',
                  'Sheffield We',
                  'Stoke',
                  'Swansea',
                  'West Brom',
                  'Wigan',
                  'Aberdeen',
                  'Celtic',
                  'Hamilton',
                  'Heart',
                  'Hibernian',
                  'Kilmarnock',
                  'Livingston',
                  'Motherwell',
                  'Rangers',
                  'Ross County',
                  'Johnstone',
                  'Mirren',
                  'Atalanta',
                  'Bologna',
                  'Brescia',
                  'Cagliari',
                  'Juventus',
                  'Fiorentina',
                  'Lazio',
                  'Roma',
                  'Inter',
                  'Milan',
                  'Genoa',
                  'Verona',
                  'Leece',
                  'Parma',
                  'Sampdoria',
                  'Sassuolo',
                  'Spal',
                  'Torino',
                  'Udinese',
                  'Napoli',
                  'Ajax',
                  'Alkmaar',
                  'Den Haag',
                  'Emmen',
                  'Feyenoord',
                  'Groningen',
                  'Heerenveen'
                  'Heracles',
                  'PSV',
                  'Sittard',
                  'Rotterdam',
                  'Twente',
                  'Utrecht',
                  'Venlo',
                  'Vitesse',
                  'Waalwijk',
                  'Willem',
                  'Zwolle']

def GI_Team_Odds(team):

    """
    Grabs the GI odds data for every match involving team, and opposition name for each match.
    """

    gi_odds_data = []

    data_length_gi = len(data_gi)

    for i in range(1, data_length_gi):
        if team in data_gi[i][10]:
            if team in data_gi[i][11]:
                #print(team, "odds are ", data_gi[i][7])
                row_number = i
                opposition = data_gi[i][12]
                gi_odds_data.append((float(data_gi[i][7]), row_number, team, opposition))
            else:
                #print(team, "odds are ", data_gi[i][9])
                row_number = i
                opposition = data_gi[i][11]
                gi_odds_data.append((float(data_gi[i][9]), row_number, team, opposition))
    return gi_odds_data


def Market_Team_Odds(team):

    """
    Grabs the odds data for every match involving team, and opposition name for each match.
    """

    market_odds_data = []

    data_length_ch = len(data_ch)
    data_length_big = len(data_big)

    for i in range(1, data_length_big):
        row_number = i
        sum_odds = float(0.0)
        if team in data_big[i][3]:
            #for j in range(0, 16, 3):
            #    sum_odds += float(data_ch[i][23+j])
            av_odds = float(data_big[i][45])
            opposition = data_big[i][4]
            market_odds_data.append((av_odds, row_number, team, opposition))
        if team in data_big[i][4]:
            #for k in range(0, 16, 3):
            #    sum_odds += float(data_ch[i][25+k])
            av_odds = float(data_big[i][47])
            opposition = data_big[i][3]
            market_odds_data.append((av_odds, row_number, team, opposition))
    #print(market_odds_data)
    return market_odds_data

def Reverse(tuples):

    """
    Reverses a tuple.
    """
    new_tup = tuples[::-1]
    return new_tup

def Compare_Odds(team):

    """
    Compares the market odds data with the GI odds data
    """

    gi_list = GI_Team_Odds(team)
    market_list = Market_Team_Odds(team)
    market_opposition_list = [(i[3], i[0], i[1]) for i in market_list]
    opposition_list = [(i[3], i[0]) for i in gi_list]
    # = [o.replace('\n', '') for o in opposition_list]
    opposition_num = len(opposition_list)
    market_num = len(market_opposition_list)

    small_length = opposition_num if opposition_num < market_num else market_num
    big_length = opposition_num if opposition_num > market_num else market_num

    matching_list = []
    #team_list = []
    for j in range(60):
        for k in range(60):
            try:
                if market_opposition_list[j][0] in opposition_list[k][0]:
                    odds_data = (market_opposition_list[j][0], 100/market_opposition_list[j][1], 100/opposition_list[k][1], market_opposition_list[j][2])
                    #team_pair = (team, market_opposition_list[j][0])
                    matching_list.append(odds_data)
            except IndexError:
                continue
                #team_list.append(team_pair)
        # print(market_opposition_list[j])
        # print(opposition_list[j])
        # match = [(market_opposition_list[j][0], market_opposition_list[j][1]) for i in opposition_list if market_opposition_list[j][0] in i]
        # if match:
        #     matching_list.append(match[0])

    #print(matching_list)
    # print(team_list)
    return matching_list

def Team_Strategy(team, wallet=20000, alpha=20, beta=1.8):

    """
    Bets on a team whenever they are undervalued on the betting markets.
    """

    tobet = 0.05*wallet
    Wallet = []

    data_length_ch = len(data_ch)
    data_length_big = len(data_big)
    bet_against = []
    matches_list = []

    for i in Compare_Odds(team):
        #print(i)

        #print(100/i[2])

        if np.any(i[2] > alpha+i[1]) and np.any((100/i[2]) < beta):
            print("Bet on ", team, "to win vs", i[0])
            bet_against.append(i[0])

    for i in range(1, data_length_big):


        # if (team, data_ch[i][4]) in strategy2():
        #     pass
        # if (data_ch[i][3], team) in strategy2():
        #     pass
        sum_home_odds = float(0.0)
        sum_away_odds = float(0.0)

        # for j in range(0, 16, 3):
        #     sum_home_odds += float(data_big[i][23+j])
        # for j in range(0, 16, 3):
        #     sum_away_odds += float(data_big[i][25+j])
        #
        # av_home_odds = sum_home_odds / 6
        # av_away_odds = sum_away_odds / 6
        av_home_odds = float(data_big[i][45])
        av_away_odds = float(data_big[i][47])
        if team in data_big[i][3] and data_big[i][4] in bet_against:
            matches_list.append((team, data_big[i][4]))
            if data_big[i][7] == 'H':
                wallet = wallet + (tobet*(av_home_odds-1))
                tobet = 0.05*wallet
                Wallet.append(wallet)
                print(team, " vs", data_big[i][4], "=", 'Win')
            else:
                wallet = wallet - tobet
                tobet = 0.05*wallet
                Wallet.append(wallet)
                print(team, " vs", data_big[i][4], "=", 'Loss')
        elif team in data_big[i][4] and data_big[i][3] in bet_against:
            matches_list.append((team, data_big[i][3]))
            if data_big[i][7] == 'A':
                wallet = wallet + (tobet*(av_away_odds-1))
                tobet = 0.05*wallet
                Wallet.append(wallet)
                print(team, " vs", data_big[i][3], "=", 'Win')
            else:
                wallet = wallet - tobet
                tobet = 0.05*wallet
                Wallet.append(wallet)
                print(team, " vs", data_big[i][3], "=", 'Loss')

    print('Wallet value after applying strategy to ', team, "=", wallet)
    return wallet, matches_list

def strategy2(alpha, beta):

    """
    Runs the betting strategy for every team in the league.
    """

    wallet = 20000
    wallet_tracker = [20000]

    for team in full_team_list:


        result = Team_Strategy(team, wallet, alpha, beta)
        wallet = result[0]
        wallet_tracker.append(result[0])



    final_value = wallet_tracker[-1]


    plt.plot(wallet_tracker)
    plt.ylabel('Wallet value')
    plt.xlabel(('Number of bets placed'))
    plt.show()
    print(final_value)

    return final_value

def alphaVary():

    """
    Varies the value of alpha whilst keeping beta constant.
    """

    Wallet = []
    for i in range(5, 36):
        testalpha = i
        Wallet.append(strategy2(testalpha, 1.8))

    plt.plot(Wallet)
    plt.ylabel('Final wallet value')
    plt.xlabel(r'$\alpha - 5$')
    plt.show()

def betaVary():

    """
    Varies the value of beta whilst keeping alpha constant.
    """

    Wallet = []
    for i in range(0, 81):
        testbeta = 1 + (0.05)*i
        Wallet.append(strategy2(23, testbeta))

    plt.plot(Wallet)
    plt.ylabel('Final wallet value')
    plt.xlabel(r'$20*(\beta-1)$')
    plt.show()


def bruteOptimise():

    """
    Optimises the betting strategy using brutce force.
    """

    f = lambda param: 1 / strategy2(param[0], param[1])
    param = brute(f, ((0, 100), (1, 10)))
    print(param)



if __name__ == "__main__":
    #GI_Team_Odds('Barnsley')
    #Market_Team_Odds('Fulham')
    #Team_Strategy('Willem', 20000, -100, 8)
    strategy2(21.05263158, 2.89473684)
    #Compare_Odds('Fulham')
    #alphaVary()
    #betaVary()
