"""
    An agent whos exploration strategy is determined by the Explicit Explore or
    Exploit (E3) Algorithm.
"""

import random
import config
from dirichlet import Dirichlet
from bayesworld import *
from strat import Strat

class E3Strat(Strat):

    def __init__(self, tm, im, m_known, color, marker=None):
        super(E3, self).init()
        self.tm = tm
        self.im = im
        self.pos = config.SS
        self.debugl = False
        self.name = "E3"
        self.color = color
        self.marker = marker
        self.known = set([])
        self.nodes = {}
        self.visit_count = {}
        self.T = 10
        self.m_known = m_known
        self.policy = {}
        self.steps_left = 0
        self.reward = 1.0
        self.discount = config.DISCOUNT_RATE

    def get_lta(self, data):
        min_count = min(data.values())
        actions = []
        for a, count in data.items():
            if count == min_count:
                actions.append(a)
        return random.sample(actions, 1)[0]

    def max_reward(self, s, V):
        max_exp_rew = -1
        for a in range(self.tm.M):
            new_states = self.im.get_known_states(a, s)
            exp = 0
            for ns in new_states:
                exp += self.im.get_prob(a, self.pos, ns) * V[ns]
            if exp > max_exp_rew:
                max_exp_rew = exp
        return max_exp_rew

    def make_exploit_strat(self):
        V = {self.T+1:{}}
        for i in self.nodes.keys():
            V[self.T+1][i] = 0.0

        for t in xrange(self.T, 0, -1):
            # Relies on reward... TODO
            V[t] = {}
            for i in self.nodes.keys():
                V[t][i] = self.reward +
                            self.discount * self.max_reward(i, V[t+1])

    def make_explore_strat():
        pass

    def step(self, step=0, last_mi=1):
        if not self.nodes.has_key(self.pos):
            self.nodes[self.pos] = {i:0 for i in range(self.im.M)}
            self.visit_count[self.pos] = 1
        elif self.pos not in self.known:
            self.visit_count[self.pos] += 1
            if self.visit_count[self.pos] > self.m_known:
                self.known.add(self.pos)

        if self.pos not in self.known:
            action = self.get_lta(self.nodes[self.pos])
            self.nodes[self.pos][a] += 1
            self.steps_left = 0 # reset
        elif:
            if not self.steps_left:
                self.steps_left = self.T
                self.policy = self.make_exploit_strat()
                if not self.policy:
                    self.policy = self.make_explore_strat()

            a = self.policy[self.pos]
            self.steps_left = self.steps_left - 1

        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)

        self.im.update(action, oldpos, self.pos)
