"""
    An agent whos exploration strategy is determined by the Boss Algorithm.
"""

import random
import config
from dirichlet import Dirichlet
from strat import Strat
from graphics import *

class BossSAStrat(Strat):

    def __init__(self, tm, im, B, color='r', marker=None):
        super(BossSAStrat, self).init(tm)
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.debugl = False
        self.name = "BOSS"
        self.color = color
        self.marker = marker
        self.known = set([])
        self.counts = {}
        self.T = 10
        self.B = B
        self.policy = {}
        self.step_num = 0
        self.reward = {config.PSI: 1.0}
        self.discount = config.DISCOUNT_RATE
        self.do_sample = True

        self.graphics = MazeGraphics(self.name, self.tm) if config.GRAPHICS else None

    def max_reward(self, s, V):
        max_exp_rew = -1
        for a in range(self.tm.M):
            new_states = self.im.get_known_states(a, s)
            exp = 0
            for ns in new_states:
                exp += self.im.get_prob(a, self.pos, ns) * max(V[ns])
            if exp > max_exp_rew:
                max_exp_rew = exp
        return max_exp_rew

    def compute_values(self):
        V = {self.T:{}}
        for s in self.im.get_states():
            V[self.T][s] = {0 for i in range(self.tm.M)}

        for t in xrange(self.T-1, -1, -1):
            V[t] = {}
            for s in self.im.get_known_states():
                for a in range(self.tm.M):
                    V[t][s][a] = self.im.get_reward(s, a) + \
                                 self.discount * self.max_reward(s, V[t+1])

            s = config.PSI
            for a in range(self.tm.M):
                V[t][s][a] = self.im.get_reward(s,a) +
                                self.discount * V[t+1][s][a]

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
        if self.graphics and config.UPDATE_STEPMI:
            self.graphics.step(step, last_mi, len(self.im.get_known_states()))

        if not self.counts.has_key(self.pos):
            self.counts[self.pos] = {i:0 for i in range(self.im.M)}
            self.reward[self.pos] = random.random()
            self.policy           = self.compute_opt_policy()

        if self.do_sample or self.step_num == self.T:
            self.policy    = self.compute_opt_policy()
            self.do_sample = False
            self.step_num = 0

        action = self.policy[self.step_num][self.pos]
        self.step_num += 1

        self.counts[self.pos][action] += 1
        if self.counts[self.pos][action] == self.B:
            self.do_sample = True

        oldpos   = self.pos
        self.pos = self.tm.take_action(self.pos, action)
        self.new_data(action, oldpos, self.pos)
        self.im.update(action, oldpos, self.pos)
