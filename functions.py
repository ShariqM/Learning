"""
    Helper functions for running the environment
"""

import math
import random
from hypothetical import *
import datetime

# Compute N choose R
def choose(n, r):
    if not n and not r:
        return 1
    if not n:
        return 0
    num = math.factorial(n)
    den = float(math.factorial(r) * math.factorial(n-r))
    return num / den

# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]

        true_over_internal = tm.get_prob(a, s, ns) / im_prob
        if true_over_internal > 0:
            x = tm.get_prob(a, s, ns) * math.log(true_over_internal, 2)
            klsum += tm.get_prob(a, s, ns) * math.log(true_over_internal, 2)

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
        imm = Hypothetical(im, a, s, ns)
        pig += im.get_prob(a, s, ns) * kl_divergence(imm, im, a, s)

    return pig

# Notes
# [1] We need to express certain outcomes as having 0 probability in 123World.
# If we don't we get in a loop where we repeatedly choose a single action that
# would gain us huge information about the model if it were possible but it's
# not.
