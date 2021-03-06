"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from functions import *
from ifunctions import *
from strat import Strat
from graphics import *
import config

from multiprocessing import Pool
import multiprocessing
import datetime

class PigVIStrat(Strat):

    def __init__(self, tm, im, color='r', PLUS=0, EXPLORER=True):
        super(PigVIStrat, self).init(tm, im)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.name = "%s-PIG" % im.get_abbr()
        #self.name = "%s-PIG" if im.has_unknown_states() else "PIG"
        self.name += "+" if PLUS else ""
        #if im.has_unknown_states():
            #self.name += " [EXPL]" if EXPLORER else " [PLAY]"
        self.color = color
        self.vi_steps = config.VI_STEPS # Number of steps to look in the future
        self.debugl = False
        self.discount = config.DISCOUNT_RATE # Discount factor for gains in future
        self.plus = PLUS # VI+ if True (uses real model)
        self.data = {}
        self.pig_cache = {}
        #name = "Explorer" if EXPLORER else "Exploiter"
        self.graphics = MazeGraphics(self.name, self.tm) if config.GRAPHICS else None
        self.explorer = EXPLORER

        self.data = []
        for s in range(self.tm.N):
            self.data.append([])
            for a in range(self.tm.get_num_actions(s)):
                self.data[s].append(0)

    def future_gain(self, i, future_v, a, s):
        if not future_v:
            return 0

        tsum = 0
        if s == config.PSI:
            return self.discount * future_v[config.PSI]
            # Maybe I should account for PSI being a known state
            #new_states = self.im.get_states()
            #prob = 1.0 / len(new_states)
            #for ns in new_states:
                #tsum += prob * future_v[ns]
            #return self.discount * tsum

        new_states = self.im.get_states(a, s)
        for ns in new_states:
            m_prob = self.im.get_prob(a, s, ns)
            if self.plus:
                m_prob = self.tm.get_prob(a, s, ns, new_states)
            tsum += m_prob * future_v[ns]

            return self.discount * tsum

    def debug(self, msg):
        if False:
            print msg

    def step(self, step, last_mi=1):
        if self.graphics and config.UPDATE_STEPMI:
            self.graphics.step(step, last_mi, len(self.im.get_known_states()))

        self.debug("Iter")
        start = datetime.datetime.now()

        for s in self.im.get_states():
            if not self.pig_cache.has_key(s):
                self.pig_cache[s] = [0] * self.tm.get_num_actions(s)
            for a in range(self.tm.get_num_actions(s)):
                if not self.pig_cache[s][a]:
                    self.pig_cache[s][a] = \
                        predicted_information_gain(self.im, a, s, self.explorer)
                    if self.graphics and config.UPDATE_PIG:
                        self.graphics.update_pig(a, s, self.pig_cache[s][a])
                #print "(a=%d, s=%d) pig=%f" % (a, s, self.pig_cache[a][s])
                #else: Validation
                    #assert self.pig_cache[a][s] ==
                    #       predicted_information_gain(self.im, a, s)

        self.debug("\t cache - %d" % (datetime.datetime.now() - start).microseconds)

        future_v = None
        for i in range(self.vi_steps):
            last_future = {} # List of Q's from the paper
            next_future_v = {}
            for s in self.im.get_states():
                last_future[s] = []
                for a in range(self.tm.get_num_actions(s)):
                    v = self.pig_cache[s][a] + self.future_gain(i, future_v, a, s)
                    last_future[s].append(v)
                    if self.graphics and config.UPDATE_VI and \
                                            i == self.vi_steps - 1:
                        self.graphics.update_vi(a, s, last_future[a][s])
                next_future_v[s] = max(last_future[s])
            future_v = next_future_v

        self.debug("\t future - %d" % (datetime.datetime.now() - start).microseconds)

        max_fgain = -10000
        best_as = []
        #print 'Start ', self.im.get_name()
        for a in range(self.tm.get_num_actions(self.pos)):
            if last_future[self.pos][a] == max_fgain:
                best_as.append(a)
            if last_future[self.pos][a] > max_fgain:
                max_fgain = last_future[self.pos][a]
                best_as = [a]
        best_a = random.sample(best_as, 1)[0]

        #print "----%s %d----" % (self.name, plus)
        #print "(s=%d, a=%d) FUTURE -" % (self.pos, best_a)
        #print_future(last_future)

        self.pig_cache[self.pos][best_a] = 0 # Cache invalidation

        ns, r = self.tm.take_action(self.pos, best_a)
        #self.im.update_information(best_a, self.pos, ns)
        self.im.update(best_a, self.pos, ns, r)
        self.new_data(best_a, self.pos, ns)
        self.pos = ns

        self.debug("\t end - %d" % (datetime.datetime.now() - start).microseconds)

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def display(self):
        self.im.display(self.name)
