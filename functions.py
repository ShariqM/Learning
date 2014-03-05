"""
    Helper functions for running the environment
"""

import math
import random
from hypothetical import *
import datetime

#klsum += tm.get_prob(a, s, ns) * abs(math.log(true_over_internal, 2))
# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]
        klsum += max(tm_prob * math.log(tm_prob / im_prob, 2), 0.0)

    return klsum

def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]
        klsum += max(tm_prob * math.log(tm_prob / im_prob, 2), 0.0)

    return klsum

def missing_information(tm, im):
    if tm.N != im.N or tm.M != im.M:
        raise Exception("Incomparable models")
    misum = 0
    for s in range(tm.N):
        for a in range(tm.M):
            misum += kl_divergence(tm, im, a, s)

    return misum

# This could be optimized, we recalculate alot, would be a little messy.
def predicted_information_gain(im, a, s):
    pig = 0
    for ns in range(im.N):
        hm = Hypothetical(im, a, s, ns)
        x = im.get_prob(a, s, ns) * kl_divergence(hm, im, a, s, False)
        pig += x

    return pig


def pig2(im, a, s):
    pig = 0
    new_states = im.get_neighbors(s, a)
    new_states.append(-1) # a new state (table)
    for ns in new_states:
        hm = Hypothetical(im, a, s, ns)
        x = im.get_prob(a, s, ns) * kl_divergence(hm, im, a, s, False)
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
