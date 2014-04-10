"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *
from ifunctions import *
from strat import Strat
from graphics import MazeGraphics

from multiprocessing import Pool
import multiprocessing
import datetime

class PigVIStrat(Strat):

    def __init__(self, tm, im, color, control=0, explorer=True, graphics=True):
        super(PigVIStrat, self).init()
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(VI%s)" % ('+' * control)
        self.color = color
        self.plansteps = 10 # Number of steps to look in the future
        self.debugl = False
        self.discount = 0.95 # Discount factor for gains in future
        self.control = control # VI+ if True (uses real model)
        self.data = {}
        self.pig_cache = [{} for a in range(self.tm.M)]
        print 'initialize'
        name = "Explorer" if explorer else "Nurterer"
        self.graphics = MazeGraphics(name, self.tm) if graphics else None
        self.explorer = explorer

        self.data = []
        for s in range(self.tm.N):
            self.data.append([])
            for a in range(4):
                self.data[s].append(0)

    def future_gain(self, i, future_v, a, s):
        if not future_v:
            return 0

        tsum = 0
        new_states = self.im.get_states()
        for ns in new_states:
            if s == -1:
                m_prob = 1 if ns == -1 else 0.001
            else:
                if self.control:
                    m_prob = self.tm.get_prob(a, s, ns, new_states)
                else:
                    m_prob = 0.001
                    if self.im.is_aware_of(a, s, ns):
                        m_prob = self.im.get_prob(a, s, ns)
            tsum += m_prob * future_v[ns]

        return self.discount * tsum

    def debug(self, msg):
        if False:
            print msg

    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        self.graphics.step(last_mi, len(self.im.get_known_states()))
        self.debug("Iter")
        start = datetime.datetime.now()

        for a in range(self.im.M):
            for s in self.im.get_states():
                if not self.pig_cache[a].has_key(s):
                    self.pig_cache[a][s] = \
                        predicted_information_gain(self.im, a, s, self.explorer)
                    self.graphics.update_pig(a, s, self.pig_cache[a][s])
                #print "(a=%d, s=%d) pig=%f" % (a, s, self.pig_cache[a][s])
                #else: Validation
                    #assert self.pig_cache[a][s] ==
                    #       predicted_information_gain(self.im, a, s)

        self.debug("\t cache - %d" % (datetime.datetime.now() - start).microseconds)

        #for control in (1, 0):
        for control in (self.control,):
            self.control = control

            future_v = None
            for i in range(self.plansteps):
                last_future = [] # List of Q's from the paper
                next_future_v = {}
                for a in range(self.im.M):
                    last_future.append({})
                    for s in self.im.get_states():
                        v = self.pig_cache[a][s] + self.future_gain(i, future_v, a, s)
                        last_future[a][s] = v
                        #if i == self.plansteps - 1:
                            #self.graphics.update_vi(a, s, last_future[a][s])
                        next_future_v[s] = max(next_future_v[s], v) if next_future_v.has_key(s) else v
                future_v = next_future_v

            self.debug("\t future - %d" % (datetime.datetime.now() - start).microseconds)

            max_fgain = -1
            best_as = []
            for a in range(self.im.M):
                if last_future[a][self.pos] == max_fgain:
                    best_as.append(a)
                if last_future[a][self.pos] > max_fgain:
                    max_fgain = last_future[a][self.pos]
                    best_as = [a]
            best_a = random.sample(best_as, 1)[0]

            #print "----%s %d----" % (self.name, control)
            #print "(s=%d, a=%d) FUTURE -" % (self.pos, best_a)
            #print_future(last_future)

        self.pig_cache[best_a].pop(self.pos) # ASSUMPTION

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.new_data(best_a, self.pos, ns)
        self.pos = ns

        self.debug("\t end - %d" % (datetime.datetime.now() - start).microseconds)

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def display(self):
        self.im.display(self.name)
