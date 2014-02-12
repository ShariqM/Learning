"""
    An agent whos exploration strategy is to choose an action at random
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

class RandomStrat():

    def __init__(self, tm, im, color, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "Random"
        self.color = color
        self.marker = marker

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def step(self):
        actions = [x for x in range(self.tm.M)]
        action = random.sample(actions, 1)[0]
        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)

        self.im.update(action, oldpos, self.pos)

    def display(self):
        self.im.display(self.name)

