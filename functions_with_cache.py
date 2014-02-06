"""
    Tried adding caching layer 2-5-14, didn't seem to help.
"""
import math
import random
from hypothetical import *
import datetime


total_time = datetime.datetime.now() - datetime.datetime.now() # 0


saved_time = 0
cache_mid = -1
cache_moves = -1
cache = []
def init_cache(tm):
    global cache
    cache = []
    for a in range(tm.M):
        cache.append([])
        for s in range(tm.N):
            cache[a].append([])
            for ns in range(tm.N):
                cache[a][s].append(0)

# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s):
    global cache
    global cache_mid
    global cache_moves
    global total_time
    global saved_time
    if cache_mid != im.mid or cache_moves != im.moves:
        init_cache(tm)

    klsum = 0
    for ns in range(tm.N):
        if not tm.is_affected_by(a, s) and cache[a][s][ns]:
            #print "using cache"
            klsum += cache[a][s][ns]
            saved_time += 0.000027
            continue

        time = datetime.datetime.now()
        true_over_internal = tm.get_prob(a, s, ns) / im.get_prob(a, s, ns)
        if true_over_internal > 0:
            val = tm.get_prob(a, s, ns) * math.log(true_over_internal, 2)
            klsum += val
            if not tm.is_affected_by(a, s):
                cache[a][s][ns] = val
        #print (datetime.datetime.now() - time)

    cache_mid = im.mid
    cache_moves = im.moves

    #if random.random() < 0.001:
        #print total_time
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
def predicted_information_gain(tm, im, a, s):
    pig = 0
    for ns in range(im.N):
        imm = Hypothetical(im, a, s, ns)
        pig += im.get_prob(a, s, ns) * kl_divergence(imm, im, a, s)
    return pig
