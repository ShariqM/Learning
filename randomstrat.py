"""
    An agent whos exploration strategy is to choose an action at random
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

class RandomStrat():

    def __init__(self, tm, color, marker, prior=0, alpha=1):
        self.tm = tm
        self.im = BayesWorld(tm) if not prior else Dirichlet(tm, alpha)
        self.pos = 0
        self.name = "Random"
        self.color = color
        self.marker = marker

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

