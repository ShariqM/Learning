"""
    An agent whos exploration strategy is determined by the Boss Algorithm.
"""

import random
import config
import pdb
from dirichlet import Dirichlet
from strat import Strat
from graphics import *
import sys

class BossSAStrat(Strat):

    def __init__(self, tm, im, B, color='r', marker=None):
        super(BossSAStrat, self).init(tm, im)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.debugl = False
        self.name = "%d-BOSS" % B
        self.color = color
        self.marker = marker
        self.known = set([])
        self.counts = {}
        self.T = 50
        self.B = B
        self.policy = {}
        self.reward = {config.PSI: 1.0}
        self.discount = config.DISCOUNT_RATE
        self.do_sample = True
        self.last_action = -1
        self.step_optimize = 99999

        self.graphics = MazeGraphics(self.name, self.tm) if config.GRAPHICS else None

    def max_reward(self, s, a, V):
        max_exp_rew = -1
        new_states = self.im.get_known_states(a, s)
        exp = 0
        for ns in new_states:
            exp += self.im.get_prob(a, s, ns) * max(V[ns].values())
        if exp > max_exp_rew:
            max_exp_rew = exp
        return max_exp_rew

    def compute_values(self):
        V = {self.T:{}}
        for s in self.im.get_states():
            V[self.T][s] = {i:0 for i in range(self.tm.M)}

        for t in xrange(self.T-1, -1, -1):
            V[t] = {}
            for s in self.im.get_known_states():
                V[t][s] = {i:0 for i in range(self.tm.M)}
                for a in range(self.tm.M):
                    V[t][s][a] = self.im.get_reward(a, s) + \
                                 self.discount * self.max_reward(s, a, V[t+1])

            s = config.PSI
            V[t][s] = {i:0 for i in range(self.tm.M)}
            for a in range(self.tm.M):
                V[t][s][a] = self.im.get_reward(a, s) + \
                                self.discount * V[t+1][s][a]
            #print "\t t=%d V=" % t, V[t]

        #pdb.set_trace()
        return V

    def compute_opt_policy(self):
        V = self.compute_values()
        policy = {}
        for t in xrange(self.T-1, -1, -1):
            policy[t] = {}
            for s in self.im.get_states():
                best_as = []
                best_val = -1.0
                for a in range(self.tm.M):
                    val = V[t][s][a]
                    if val == best_val:
                        best_as.append(a)
                    elif val > best_val:
                        best_val = val
                        best_as = [a]
                policy[t][s] = random.sample(best_as, 1)[0]

        return policy

    def step(self, step=0, last_mi=1):
        self.last_action = random.randint(0,100)
        if self.graphics and config.UPDATE_STEPMI:
            self.graphics.step(step, last_mi, len(self.im.get_known_states()))

        if not self.counts.has_key(self.pos):
            self.counts[self.pos] = {i:0 for i in range(self.im.M)}
            self.reward[self.pos] = random.random()

        #if self.pos not in self.im.get_states() or \
                                            # self.step_num == self.T or \
        if self.do_sample or self.pos not in self.policy[0].keys():
            self.policy    = self.compute_opt_policy()
            self.do_sample = False

        action = self.policy[0][self.pos]

        self.counts[self.pos][action] += 1
        if self.counts[self.pos][action] == self.B:
            self.do_sample = True

        oldpos   = self.pos
        self.pos, r = self.tm.take_action(self.pos, action)
        self.new_data(action, oldpos, self.pos)
        self.im.update(action, oldpos, self.pos, r)

    def la(self):
        sys.stdout.write("la=%d\n" % self.last_action)
        sys.stdout.flush()
