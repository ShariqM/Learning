"""
    Helper functions for running the environment
"""

import math
import random
from hypothetical import *
import datetime

UNK_PROB = float("1e-5")
# klsum += tm.get_prob(a, s, ns) * abs(math.log(true_over_internal, 2))
# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]
        klsum += max(tm_prob * math.log(tm_prob / im_prob, 1.1), 0.0)

    return klsum

# A more flexible divergence that can deal with unknown states
# is_aware_of is used to make the DirichletProcess probabilities sum to 1
def sm_divergence(tm, im, a, s, debug=False):
    div = 0
    for ns in tm.get_states(a, s):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0:
            continue
        im_prob = UNK_PROB
        if im.has_state(s) and im.is_aware_of(a, s, ns):
            im_prob = im.get_prob(a, s, ns) if im.is_aware_of(a, s, ns) else UNK_PROB
        div += max(tm_prob * math.log(tm_prob / im_prob, 2), 0.0)
    return div

# TODO Need to make this an argument to runner
def divergence(tm, im, a, s, debug=False):
    if True:
        return sm_divergence(tm, im, a, s, debug)
    else:
        return kl_divergence(tm, im, a, s, debug)

def missing_information(tm, im):
    misum = 0
    for s in range(tm.N):
        for a in range(tm.M):
            misum += divergence(tm, im, a, s)
    return misum

# This could be optimized, we recalculate alot, would be a little messy.
def predicted_information_gain(im, a, s):
    pig = 0

    if s == -1:
        return math.log(1.0 / UNK_PROB, 2) #Hmm....
    for ns in im.get_states(a, s):
        hm = Hypothetical(im, a, s, ns)
        x = im.get_prob(a, s, ns) * divergence(hm, im, a, s, False)
        pig += x

    return pig

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

# Notes
# [1] We need to express certain outcomes as having 0 probability in 123World.
# If we don't we get in a loop where we repeatedly choose a single action that
# would gain us huge information about the model if it were possible but it's
# not.
