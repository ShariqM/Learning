"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

class PigGreedyVIStrat():

    def __init__(self, tm, color, prior=0, alpha=1):
        self.tm = tm
        self.im = BayesWorld(tm) if not prior else Dirichlet(tm, alpha)
        self.pos = 0
        self.name = "PIG(VI)"
        self.color = color
        self.plan = []
        self.plansteps = 3 # Number of steps to look in the future
        self.discount = 0.95 # Discount factor for gains in future

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def best_value(self, future, s):
        tmax = -1
        for a in range(self.im.M):
            if future[a][s] > tmax:
                tmax = future[a][s]
        return tmax

    def future_gain(self, i, all_futures, a, s):
        if i == 0:
            return 0

        tsum = 0
        for ns in range(self.im.N):
            tsum += self.im.get_prob(a, s, ns) * \
                    self.best_value(all_futures[i-1], ns)
        return self.discount * tsum

    def step(self):
        if len(self.plan) != 0:
            ns = self.tm.take_action(self.pos, self.plan[0])
            self.im.update(best_a, self.pos, ns)
            self.pos = ns
            return

        all_futures = [] # List of Q's from the paper
        for i in range(self.plansteps):
            all_futures.append([])
            for a in range(self.im.M):
                all_futures[i].append([])
                for s in range(self.im.N):
                    all_futures[i][a].append([])
                    #print i, a, s, all_futures
                    all_futures[i][a][s] = predicted_information_gain(self.im, a, s) \
                        + self.future_gain(i, all_futures, a, s)

        max_fgain = -1
        best_a = -1
        future = all_futures[self.plansteps - 1]
        for a in range(self.im.M):
            if future[a][self.pos] > max_fgain:
                max_fgain = future[a][self.pos]
                best_a = a

        #print "(a=%d, s=%d) pig=%d l=%d" % (best_a, self.pos, max_gain, \
                    #len(best_as))
        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

    def display(self):
        self.im.display(self.name)

