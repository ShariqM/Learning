"""
    A Chain Strat runs the optimum policy, i.e. action 0 always.
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

class ChainStrat(Strat):

    def __init__(self, tm, im):
        super(ChainStrat, self).init(tm)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "ChainStrat"

    def step(self, step, last_mi):
        action = 0
        ns, r = self.tm.take_action(self.pos, action)
        self.im.update(action, self.pos, ns, r)
        self.pos = ns
