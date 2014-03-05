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
        self.total_obs = []
        self.alpha = 0.25

        for action in range(M):
            self.data.append({})
            self.total_obs.append(0)
            self.actions.append({})

    # Dirichlet distribution with alpha=0.25
    def get_prob(self, a, ns):
        if not in self.data[a].has_key(ns):
            return self.alpha / (self.total_obs[a] - 1 + self.alpha)
        return self.data[a][ns] / (self.total_obs[a] - 1 + self.alpha)

    def get_neighbors(self, a):
        return self.data[a].keys()

    def update(self, a, ns):
        prev = self.data[a][ns] if self.data[a].has_key(ns) else 0
        self.data[a][ns] = prev + 1
        self.total_obs[a] = self.total_obs[a] + 1
        self.neighbors.append(ns)

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.data[a].pop(ns)
        else:
            self.data[a][ns] = self.data[a][ns] - 1
        self.total_obs[a] = self.total_obs[a] - 1
        self.neighbors.append(ns)
