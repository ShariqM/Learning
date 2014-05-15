"""
    A DyStrat runs one strategy for a period of steps and then switches to a
    second.
"""

import random
from functions import *
from ifunctions import *
from strat import Strat
from graphics import *
import config

import datetime

class DyStrat(Strat):

    def __init__(self, tm, im, astrat, bstrat, step_switch):
        super(DyStrat, self).init(tm)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "DyStrat(%s and %s)" % (astrat.name, bstrat.name)
        self.strat = astrat
        self.bstrat = bstrat
        self.step_switch = step_switch

    def step(self, step, last_mi=1):
        if step == self.step_switch:
            self.strat = self.bstrat
            print 'SWITCH'
        self.strat.step(step, last_mi)
        print "reward = ", self.im.reward
