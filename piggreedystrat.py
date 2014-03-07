"""
    A PigGreedy agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

class PigGreedyStrat():

    def __init__(self, tm, im, proc, color, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(greedy)"
        if proc:
            self.name += " [proc]"
        self.proc = proc
        self.color = color
        self.marker = marker
        self.data = {}

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    # Look for the action that results in the most pig and then
    # take it.
    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        max_gain = -1
        best_as = []
        for a in range(self.im.M):
            pig = predicted_information_gain(self.im, a, self.pos)
            #print '\tpig=%f' % pig
            if pig > max_gain:
                max_gain = pig
                best_as = [a]
            if pig == max_gain:
                best_as.append(a)
        # This prevents us from picking the same action forever
        best_a = random.sample(best_as, 1)[0]

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

        if not self.data.has_key((self.pos, best_a)):
            self.data[(self.pos, best_a)] = 0
        self.data[(self.pos, best_a)] = self.data[(self.pos, best_a)] + 1
        print self.data
        print "(s=%d, a=%d, ns=%d)" % (self.pos, best_a, ns)

    def display(self):
        print self.data
        self.im.display(self.name)
