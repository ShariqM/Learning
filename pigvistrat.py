"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *
from strat import Strat

from multiprocessing import Pool
import multiprocessing
import datetime

class PigVIStrat(Strat):

    def __init__(self, tm, im, color, control=False, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(VI+)" if control else "PIG(VI)"
        self.color = color
        self.marker = marker
        self.plansteps = 10 # Number of steps to look in the future
        self.discount = 0.95 # Discount factor for gains in future
        self.control = control # VI+ if True (uses real model)
        self.data = {}
        self.pig_cache = [{} for a in range(self.tm.M)]

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def best_value(self, future, s):
        tmax = -1
        for a in range(self.im.M):
            tmax = max(future[a][s],tmax)
        return tmax

    def future_gain(self, i, all_futures, a, s):
        if i == 0:
            return 0

        tsum = 0
        num_states = len(self.im.get_states())
        for ns in self.im.get_states():
            m = self.tm if self.control else self.im
            m_prob = 1.0/num_states if s == -1 else m.get_prob(a, s, ns)
            tsum += m_prob * self.best_value(all_futures[i-1], ns)

        return self.discount * tsum

    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        #print "Iter"
        start = datetime.datetime.now()

        for a in range(self.im.M):
            for s in self.im.get_states():
                if self.pig_cache[a].has_key(s):
                    continue
                self.pig_cache[a][s] = predicted_information_gain(self.im, a, s)
        #print "\t cache - ", (datetime.datetime.now() - start).microseconds

        pigs = self.pig_cache
        all_futures = [] # List of Q's from the paper
        for i in range(self.plansteps):
            all_futures.append([])
            for a in range(self.im.M):
                all_futures[i].append({})
                for s in self.im.get_states():
                    all_futures[i][a][s] = pigs[a][s] + \
                        self.future_gain(i, all_futures, a, s)

        #print "\t future - ", (datetime.datetime.now() - start).microseconds

        max_fgain = -1
        best_a = -1
        future = all_futures[self.plansteps - 1]
        for a in range(self.im.M):
            if future[a][self.pos] > max_fgain:
                max_fgain = future[a][self.pos]
                best_a = a

        self.pig_cache[best_a].pop(self.pos) # ASSUMPTION

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

        #print "\t end - ", (datetime.datetime.now() - start).microseconds

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def display(self):
        self.im.display(self.name)
