"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from functions import *
from bayesworld import *

class UnembodiedStrat():

    def __init__(self, tm, im, color, marker=None):
        self.tm = tm
        self.im = im
        self.name = "Unembodied"
        self.color = color
        self.marker = marker

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    # Look for the (state, action) pair that results in the most pig and then
    # take it. This is pretty slow...
    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        max_gain = 0
        best_a = 0
        best_s = 0
        for a in range(self.im.M):
            for s in range(self.im.N):
                pig = predicted_information_gain(self.im, a, s)
                if pig > max_gain:
                    max_gain = pig
                    best_a = a
                    best_s = s
        #print '(a=%d, s=%d) max_gain =%f' % (best_a, best_s, max_gain)
        x = self.compute_mi()
        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
        #print 'gained: ', self.compute_mi() - x

    def display(self):
        self.im.display(self.name)

