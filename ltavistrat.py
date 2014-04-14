"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that it has taken the least from any given state
"""

import random
import math
from dirichlet import Dirichlet
from bayesworld import *
from strat import Strat

from multiprocessing import Pool
import multiprocessing
import datetime
import config
import pdb

class LTAVIStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        super(LTAVIStrat, self).init()
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "LTA (VI)"
        self.vi_steps = config.VI_STEPS
        #self.debugl = True
        self.debugl = False
        self.discount = config.DISCOUNT_RATE
        self.color = color
        self.marker = marker
        self.nodes = {}
        self.node_vals = {}
        for s in self.im.get_states():
            self.nodes[s] = [0 for i in range(self.im.M)]

    def get_lta(self, data):
        max_count = min(data.values())
        for a, count in data.items():
            if count == max_count:
                return a

    def future_gain(self, i, future_v, a, s):
        if not future_v:
            return 0

        tsum = 0
        new_states = self.im.get_states()
        for ns in new_states:
            tsum += self.im.get_prob(a, s, ns) * future_v[ns]

        return self.discount * tsum

    def step(self, last_mi=1):
        if not self.nodes.has_key(self.pos):
            self.nodes[self.pos] = {i:0 for i in range(self.im.M)}

        future_v = None
        for i in range(self.vi_steps):
            last_future = [] # List of Q's from the paper
            next_future_v = {}
            for a in range(self.im.M):
                last_future.append({})
                for s in self.im.get_states():
                    v = 100.0 / (sq(self.nodes[s][a]) + 1.0) + \
                                self.future_gain(i, future_v, a,  s)
                    last_future[a][s] = v
                    next_future_v[s] = max(next_future_v[s], v)  \
                                if next_future_v.has_key(s) else v

            future_v = next_future_v

        max_fgain = -1
        best_a = -1
        for a in range(self.im.M):
            if last_future[a][self.pos] > max_fgain:
                max_fgain = last_future[a][self.pos]
                best_a = a

        #print "Dump"
        #for s in self.im.get_states():
            #for a in range(self.im.M):
                #print "\t(s=%d, a=%d) d=%d v = " % (s,a,self.nodes[s][a]), \
                        #100.0 / (sq(self.nodes[s][a]) + 1.0)

        self.nodes[self.pos][best_a]  += 1

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.debug("(a=%d, s=%d, ns=%d)" % (best_a,self.pos,ns))
        self.pos = ns

def sq(x):
    return math.pow(x, 2)
