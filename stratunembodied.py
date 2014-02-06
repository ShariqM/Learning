"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from functions import *

class StratUnembodied():

    def __init__(self, tm):
        self.tm = tm
        self.im = Dirichlet(tm)

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    # Look for the (state, action) pair that results in the most pig and then
    # take it. This is pretty slow...
    def step(self):
        max_gain = 0
        best_a = 0
        best_s = 0
        time = datetime.datetime.now()
        for a in range(self.im.M):
            for s in range(self.im.N):
                pig = predicted_information_gain(self.tm, self.im, a, s)
                if pig > max_gain:
                    max_gain = pig
                    best_a = a
                    best_s = s

        ns = self.tm.take_action(best_s, best_a)

        orig = self.compute_mi()
        self.im.update(best_a, best_s, ns)
        new = self.compute_mi()
        #print "U - gained=%f" % (new-orig)

    def display(self):
        self.im.display("Unembodied")

