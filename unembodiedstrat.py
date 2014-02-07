"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from functions import *
from bayesworld import *

class StratUnembodied():

    def __init__(self, tm, alpha):
        self.tm = tm
        self.im = BayesWorld(tm)
        self.name = "Unembodied"

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    # Look for the (state, action) pair that results in the most pig and then
    # take it. This is pretty slow...
    def step(self):
        #self.tm.display()
        #self.display()
        max_gain = 0
        best_a = 0
        best_s = 0
        time = datetime.datetime.now()
        for a in range(self.im.M):
            for s in range(self.im.N):
                pig = predicted_information_gain(self.tm, self.im, a, s)
                #print "PIG: %d (%d---%d)" % (pig, s, a)
                if pig > max_gain:
                    max_gain = pig
                    best_a = a
                    best_s = s

        before = self.compute_mi()
        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
        after = self.compute_mi()
        #print "pig=%d, %d-%d->%d" % (max_gain, best_s, best_a, ns)
        #if before == after:
            #raise Exception( "No information gained a=%d s=%d ns=%d" %
            #(best_a,best_s, ns))


    def display(self):
        self.im.display(self.name)

