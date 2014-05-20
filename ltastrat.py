"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that it has taken the least from any given state
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from strat import Strat

from multiprocessing import Pool
import multiprocessing
import datetime
import pdb

class LTAStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        super(LTAStrat, self).init(tm)
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "LTA"
        self.color = color
        self.marker = marker
        self.nodes = {}
        self.debugl = False

    def get_lta(self, data):
        max_count = min(data.values())
        for a, count in data.items():
            if count == max_count:
                return a

    def step(self, step=0, last_mi=1):
        if not self.nodes.has_key(self.pos):
            self.nodes[self.pos] = {i:0 for i in range(self.im.M)}

        a = self.get_lta(self.nodes[self.pos])
        self.nodes[self.pos][a] += 1

        ns, reward = self.tm.take_action(self.pos, a)
        self.im.update(a, self.pos, ns, reward)
        self.debug("(a=%d, s=%d, ns=%d)" % (a,self.pos,ns))
        self.pos = ns
