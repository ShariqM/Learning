"""
    A DirichletNode encodes the internal probability distribution model for a
    single node. Bayesian updates described in section (1) and (2) of Appendix A2.
"""

import random
import math

class DirichletNode:

    def __init__(self, M, N, neighbors):
        self.M = M
        self.N = N
        self.actions = []
        self.data = []
        self.total_obs = []
        self.neighbors = neighbors
        self.Ns = len(set(self.neighbors)) # Number of unique neighbors
        self.alpha = 0.25

        for action in range(M):
            self.data.append([0 for x in range(N)])
            self.total_obs.append(0)
            self.actions.append([x for x in range(N)])

    # Dirichlet distribution with alpha=0.25 (Equation 14)
    def get_prob(self, a, ns):
        if ns not in self.neighbors:
            # Peeking into real model... kinda hacky
            return 0.0

        osum = 0
        for os in range(self.N):
            osum += self.data[a][os]
        x = (self.data[a][ns] + self.alpha) / (self.Ns * self.alpha + osum)
        return x

    def update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] + 1
        self.total_obs[a] = self.total_obs[a] + 1

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] - 1
        self.total_obs[a] = self.total_obs[a] - 1
