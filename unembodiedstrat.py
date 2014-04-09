"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG

    Notes
    - MultiProcess results in a
        - ~30% performance gain with 4 CPUs on 123World
        - ~100% performance gain with 4 CPUs on Maze
    - There is no concurrency control so we are assuming concurrent PIG
      computations are independent.
"""

import random
from dirichlet import Dirichlet
from functions import *
from ifunctions import *
from bayesworld import *
from strat import Strat
import datetime
import pdb

from multiprocessing import Pool
import multiprocessing

class UnembodiedStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        self.tm = tm
        self.im = im
        self.name = "Unembodied"
        self.color = color
        self.debugl = False
        self.marker = marker
        self.pig_cache = [{} for a in range(self.tm.M)]

    # Take the (state, action) that results in the most pig
    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return

        max_gain, best_a, best_s = (-5.0, -5, -5)
        for a in range(self.im.M):
            for s in self.im.get_known_states():
                if not self.pig_cache[a].has_key(s):
                    self.pig_cache[a][s] = \
                        predicted_information_gain(self.im, a, s)
                if self.pig_cache[a][s] > max_gain:
                    max_gain, best_a, best_s = (self.pig_cache[a][s], a, s)

        self.pig_cache[best_a].pop(best_s) # ASSUMPTION

        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
