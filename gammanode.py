"""
    A GammaProcessNode encodes the internal probability distribution model for a
    single node.
"""

import random
import math

class GammaProcessNode:

    def __init__(self, M, gamma=3.5):
        self.data = []
        self.obs_num = []
        self.M = M
        self.total_reward = [0 for i in range(self.M)]

        assert type(gamma) != int
        self.gamma = gamma

        for action in range(self.M):
            self.data.append({}) # Number of times (s,a,ns) has been observed
            self.obs_num.append(0) # Num of times (s,a) has been observed

    def get_states(self, a):
        return self.data[a].keys()

    def is_aware_of(self, a, ns):
        return self.data[a].has_key(ns)

    def get_prob_psi(self, a):
        return 1.0 - math.pow(self.gamma/(1.0+self.gamma), 1.0/self.obs_num[a])

    def get_prob_first_obs(self):
        return 1.0 - self.gamma/(1.0 + self.gamma)

    # Generalization of CRP
    def get_prob(self, a, ns):
        if not self.obs_num[a]:
            return 1.0
        p = self.get_prob_psi(a)
        if not self.data[a].has_key(ns):
            return p
        return (1.0 - p) * self.data[a][ns] / self.obs_num[a]

    def get_reward(self, a):
        if not self.obs_num[a]:
            return 0.0
        return self.total_reward[a] / self.obs_num[a] # Mean reward

    def update(self, a, ns, r=0.0):
        prev = self.data[a][ns] if self.data[a].has_key(ns) else 0
        self.data[a][ns] = prev + 1
        self.obs_num[a] = self.obs_num[a] + 1
        self.total_reward[a] += r

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.data[a].pop(ns)
        else:
            self.data[a][ns] = self.data[a][ns] - 1
        self.obs_num[a] = self.obs_num[a] - 1

    def stats(self):
        for a in range(self.M):
            print 'a=%d ->' % a, self.data[a]
