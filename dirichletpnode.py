"""
    A DirichletProcessNode encodes the internal probability distribution model for a
    single node. This is closely related to the Chinese Restaurant Process.
"""

import random
import math

class DirichletProcessNode:

    def __init__(self, M):
        self.M = M
        self.actions = []
        self.data = []
        self.obs_num = []
        self.alpha = 0.25

        for action in range(M):
            self.data.append({})
            self.obs_num.append(1)
            self.actions.append({})

    def get_states(self, a):
        return self.data[a].keys()

    def is_aware_of(self, a, ns):
        return self.data[a].has_key(ns)

    # Dirichlet distribution with alpha=0.25
    def get_prob(self, a, ns):
        if not self.data[a].has_key(ns):
            return self.alpha / (self.obs_num[a] - 1 + self.alpha)
        return self.data[a][ns] / (self.obs_num[a] - 1 + self.alpha)

    def update(self, a, ns):
        prev = self.data[a][ns] if self.data[a].has_key(ns) else 0
        self.data[a][ns] = prev + 1
        self.obs_num[a] = self.obs_num[a] + 1

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.data[a].pop(ns)
        else:
            self.data[a][ns] = self.data[a][ns] - 1
        self.obs_num[a] = self.obs_num[a] - 1
