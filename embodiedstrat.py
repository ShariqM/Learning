"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

class EmbodiedStrat():

    def __init__(self, tm, color):
        self.tm = tm
        self.im = BayesWorld(tm)
        self.pos = 0
        self.name = "Embodied"
        self.color = color

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    # Look for the action that results in the most pig and then
    # take it.
    def step(self):
        max_gain = 0
        best_a = 0
        for a in range(self.im.M):
            pig = predicted_information_gain(self.im, a, self.pos)
            if pig > max_gain:
                max_gain = pig
                best_a = a

        print "(a=%d, s=%d)" % (best_a, self.pos)
        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

    def display(self):
        self.im.display(self.name)

