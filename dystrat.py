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
import pdb
import sys

class DyStrat(Strat):

    def __init__(self, tm, im, astrat, bstrat, step_switch):
        super(DyStrat, self).init(tm)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "DyStrat[SS=%d] (%s and %s)" % (step_switch, astrat.name, bstrat.name)
        self.strat = astrat
        self.bstrat = bstrat
        self.step_switch = step_switch
        # We have to keep track of this b/c MultProc screw it up as arg
        self.ls = -1

    def step(self, step, last_mi):
        self.ls = step
        if step == self.step_switch:
            self.strat = self.bstrat

        self.strat.step(step, last_mi)
        #if step >= 999:
            #s = "ss=%d reward = %f" % (self.step_switch, self.im.total_reward)
            #sys.stdout.write(s)
            #sys.stdout.flush()
