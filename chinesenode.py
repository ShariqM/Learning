"""
    A DirichletProcessNode encodes the internal probability distribution model for a
    single node. This is closely related to the Chinese Restaurant Process.
"""

import random
import math

class ChineseRProcessNode:

    def __init__(self, M, theta=3.0, alpha=0.0):
        self.data = []
        self.obs_num = []
        self.M = M
        self.total_reward = [0 for i in range(self.M)]

        assert type(alpha) != int
        assert type(theta) != int
        self.theta = theta # Strength parameter
        self.alpha = alpha # Discount parameter
        self.done = False

        for action in range(self.M):
            self.data.append({}) # Number of times (s,a,ns) has been observed
            self.obs_num.append(0) # Num of times (s,a) has been observed

    def get_states(self, a):
        return self.data[a].keys()

    def is_aware_of(self, a, ns):
        return self.data[a].has_key(ns)

    def get_prob_first_obs(self):
        return (1.0 - self.alpha) / (1.0 + self.theta)

    # Generalization of CRP
    def get_prob(self, a, ns):
        if not self.data[a].has_key(ns):
            ntables = len(self.data[a])
            return (self.theta + ntables * self.alpha) / \
                    (self.obs_num[a] + self.theta)
        return (self.data[a][ns] - self.alpha) / (self.obs_num[a] + self.theta)

    def get_reward(self, a):
        return self.reward[a] / self.obs_num[a] # Mean reward

    def update(self, a, ns, r=0):
        prev = self.data[a][ns] if self.data[a].has_key(ns) else 0
        #if self.obs_num[a] == 5 and not self.done:
            #self.done = True
            #print self.data[a]
        self.data[a][ns] = prev + 1
        self.obs_num[a] = self.obs_num[a] + 1
        self.reward[a] += r

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.data[a].pop(ns)
        else:
            self.data[a][ns] = self.data[a][ns] - 1
        self.obs_num[a] = self.obs_num[a] - 1

    def stats(self):
        for a in range(self.M):
            print self.data[a]
