"""
    An agent whos exploration strategy is built for bayesian inference on 123
    worlds
"""

import random
from dirichlet import Dirichlet
from functions import *

class StratRandom():

    def __init__(self, tm, alpha):
        self.tm = tm
        self.im = Dirichlet(tm, alpha)
        self.pos = 0
        self.name = "Random"

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def step(self):
        states = [x for x in range(self.tm.M)]
        action = random.sample(states, 1)[0]
        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)

        orig = self.compute_mi()
        self.im.update(action, oldpos, self.pos)
        new = self.compute_mi()

    def display(self):
        self.im.display(self.name)

