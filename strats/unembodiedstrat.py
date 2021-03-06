"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG
"""

import random
from functions import *
from ifunctions import *
from strat import Strat
import datetime
import pdb

from multiprocessing import Pool
import multiprocessing

class UnembodiedStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        super(UnembodiedStrat, self).init(tm, im)
        self.tm = tm
        self.im = im
        self.name = "Unembodied"
        self.color = color
        self.debugl = False
        self.marker = marker
        self.pig_cache = [{} for a in range(self.tm.M)]

    # Take the (state, action) that results in the most pig
    def step(self, step=0, last_mi=1):
        max_gain, best_a, best_s = (-5.0, -5, -5)
        for s in self.im.get_known_states():
            for a in range(self.tm.get_num_actions(s)):
                if not self.pig_cache[a].has_key(s):
                    self.pig_cache[a][s] = \
                        predicted_information_gain(self.im, a, s, False)
                if self.pig_cache[a][s] > max_gain:
                    max_gain, best_a, best_s = (self.pig_cache[a][s], a, s)

        self.pig_cache[best_a].pop(best_s) # Cache invalidation assumption

        ns, r = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns, r)
