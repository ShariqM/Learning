"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that is chosen via Counter-Based Exploration
"""

import random
import config
from dirichlet import Dirichlet
from bayesworld import *
from strat import Strat

from multiprocessing import Pool
import multiprocessing
import datetime
import pdb
import sys

class CBStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        super(CBStrat, self).init(tm, im)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "CB"
        self.color = color
        self.marker = marker
        self.nodes = {}
        self.counts = {}
        self.debugl = False

    # Choose actions that lead to a state with low *expected* count
    def get_cba(self):
        best_as = []
        min_exp_count = sys.maxint
        for a in range(self.tm.M):
            new_states = self.im.get_known_states(a, self.pos)
            exp = 0
            for ns in new_states:
                exp += self.im.get_prob(a, self.pos, ns) * self.counts[ns]

            if exp == min_exp_count:
                best_as.append(a)
            elif exp < min_exp_count:
                min_exp_count = exp
                best_as = [a]
        return random.sample(best_as, 1)[0]

    def step(self, step=0, last_mi=1):
        if not self.nodes.has_key(self.pos):
            self.counts[self.pos] = 1

        a = self.get_cba()

        ns, r = self.tm.take_action(self.pos, a)
        self.im.update(a, self.pos, ns, r)
        self.debug("(a=%d, s=%d, ns=%d)" % (a,self.pos,ns))
        self.pos = ns
