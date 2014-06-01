"""
    An agent whos exploration strategy is to choose an action at random
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *
from strat import Strat
import config

class RandomStrat(Strat):

    def __init__(self, tm, im, color='r', marker=None):
        super(RandomStrat, self).init(tm, im)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "Random"
        self.color = color
        self.marker = marker

    def step(self, step=0, last_mi=1):
        actions = [x for x in range(self.tm.M)]
        action = random.sample(actions, 1)[0]
        ns, r = self.tm.take_action(self.pos, action)
        self.im.update(action, self.pos, ns, r)
        self.pos = ns
