#!/usr/bin/env python

"""
Loads Betfair Data.
"""

import tarfile
import os
import bz2
import sys
import json
import pickle

outputdir = "bin2"
cnt = 0   # nr of files visited

print("""Make sure to empty the output directory before running
this script (this is because existing bin's will be merged)""")

def mergeEvents(E1, E2):
    """
    Merges events.
    """
    E = E1
    # TODO: can check consistency of other fields here
    o = E1['odds'] + E2['odds']
    o.sort(key=lambda val: val[0])
    E['odds'] = o
    return E

tar = tarfile.open("data.tar")
for member in tar:
    #print(member)
    f = tar.extractfile(member)
    content = f.read()
    c = str(bz2.decompress(content))[2:-1]

    eventId = 0

    inPlayTime = 0
    playernames = {}   # dictionary of player names, where keys are the ids
    playerstatus = {}  # dictionary of player status (ACTIVE, WINNER, LOSER), where keys are the ids
    odds = {}   # dictionary of odds at current time, where keys are the ids
    mccnt = 0   # nr of market changes listed in the current file
    Event = {}  # Dictionary of the event data
    oddarr = [] # array of odds (timestamped)

    for line in c.split("\\n"):
        if not line:
            continue
        line = line.encode('unicode_escape')
        try:
            pline = json.loads(line, strict=False)
        except:
            print("Error when processing this line:", line)
            continue
        pt = pline['pt'] # time stamp
        mc = pline['mc'][0] # market change information

        if 'marketDefinition' in mc:
            md = mc['marketDefinition']
            if 'eventId' in md:
                eventId = md['eventId']
            if 'runners' in md:
                for r in md['runners']:
                    playernames[r['id']] = r['name']
                    playerstatus[r['id']] = r['status']
            if 'inPlay' in md and inPlayTime == 0:
                if md['inPlay']:
                    inPlayTime = pt

        if 'rc' in mc:
            rc = mc['rc']  # market move
            for m in rc:
                odds[m['id']] = m['ltp']

            if len(odds) == 2:
                mccnt += 1
                oddlst = [v for _, v in sorted(odds.items())]
                oddlst.insert(0, pt)
                oddarr.append(oddlst)

    Event['names'] = [v for _, v in sorted(playernames.items())]
    Event['status'] = [v for _, v in sorted(playerstatus.items())]
    Event['tsPlay'] = inPlayTime
    Event['odds'] = oddarr

    filename = outputdir + '/' + eventId + '.bin'
    # check if file exists
    try:
        E = pickle.load(open(filename, 'rb'))

        if len(E['odds']) > 0 and len(Event['odds']) > 0:
            pass
            #print("merging nontrivial Event files!!!!", len(E['odds']), len(Event['odds']))

        Event = mergeEvents(E, Event)
        pickle.dump(Event, open(filename, 'wb'))

    except:
        pickle.dump(Event, open(filename, 'wb'))
        #print("  new file created")

    cnt += 1
    if cnt > 100000000000:
        break

tar.close()
