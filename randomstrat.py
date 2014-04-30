"""
    An agent whos exploration strategy is to choose an action at random
"""

import random
import config
from dirichlet import Dirichlet
from bayesworld import *
from strat import Strat

class RandomStrat(Strat):

    def __init__(self, tm, im, color, marker=None):
        super(RandomStrat, self).init()
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.debugl = False
        self.name = "Random"
        self.color = color
        self.marker = marker

    def step(self, step=0, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        actions = [x for x in range(self.tm.M)]
        action = random.sample(actions, 1)[0]
        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)

        self.im.update(action, oldpos, self.pos)
