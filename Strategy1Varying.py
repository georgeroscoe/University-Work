#!/usr/bin/env python

"""
Run through a variety of different alpha/beta values for the strategy.
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import PLDataLoad

pl1819_file = open('PL1819Data.csv')
reader = csv.reader(pl1819_file)
pl1819 = list(reader)

pl1718_file = open('pl1718Data.csv')
reader = csv.reader(pl1718_file)
pl1718 = list(reader)

pl1617_file = open('pl1617Data.csv')
reader = csv.reader(pl1617_file)
pl1617 = list(reader)


Wallet = []
tuple_list = []
for i in range(0, 2000):
    alph = 1 + (0.0005*i)
    beta = alph*1.05
    Wallet.append(PLDataLoad.Strategy1(alph, beta, pl1718))

    tuple_list.append((i, PLDataLoad.Strategy1(alph, beta, pl1718)))


x, y = zip(*tuple_list)

print(np.corrcoef(x, y))


plt.figure(figsize=(10, 7), dpi=80, facecolor='w', edgecolor='k')
#plt.xlim(0, 380)
plt.plot(Wallet)
plt.ylabel('Wallet value')
plt.xlabel((r'$2000*(\alpha-1)$'))


plt.title(r'Wallet value after each bet with varied $\alpha$', fontsize=14)
plt.show()
