"""
    Helper functions for running the environment
"""

import math
import random

# Compute N choose R
def choose(n, r):
    if not n and not r:
        return 1
    if not n:
        return 0
    num = math.factorial(n)
    den = float(math.factorial(r) * math.factorial(n-r))
    return num / den

def print_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze)):
            print maze[i][j],
        print

def print_future(future):
    #print "\n-----FUTURE-----"
    nfuture = {}
    for a in range(len(future)):
        #print "a=%d" % a
        for pos in future[a].keys():
            if not nfuture.has_key(pos):
                nfuture[pos] = []
            nfuture[pos].append(future[a][pos])
            #print "\ts=%d" % pos, future[a][pos]

    for s in nfuture.keys():
        print "s=%d" % s
        a = 0
        for v in nfuture[s]:
            print "\t(a=%d) ->" % (a), nfuture[s][a]
            a = a + 1

def print_pig(pigs):
    print "\n-----PIGS-----"
    a = 0
    for data in pigs:
        print "a=%d" % a
        for s, val in data.items():
            print "\t(a=%d, s=%d) ->" % (a, s), pigs[a][s]
        a = a + 1

def sample(dist):
    r = random.random()
    tsum = 0.0
    for i in range(len(dist)):
        tsum += dist[i]
        if r <= tsum:
            return i
    print 'tsum was', tsum
    return 1 - range(len(dist))

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
