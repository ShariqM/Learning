"""
    A dirichlet node calculates probability of entering a new node based on it's
    data. Its data is updated everytime it enters a new state.
"""

import random
import math

class DirichletNode:

    def __init__(self, M, N, index, alpha, debug=False):
        self.M = M
        self.N = N
        self.index = index
        self.actions = []
        self.data = []
        self.total_obs = []
        self.debug = debug
        self.alpha = alpha

        for action in range(M):
            self.data.append([0 for x in range(N)])
            self.total_obs.append(0)
            self.actions.append([x for x in range(N)])

    # Dirichlet distribution with alpha=1, see equation 13 in the appendix
    def get_prob(self, a, ns):
        return (self.alpha + self.data[a][ns]) / (self.total_obs[a] + self.N*self.alpha)

    def get_sprob(self, a, ns):
        return "(%d/%d)" % (self.data[a][ns] + 1, self.total_obs[a] + self.N)

    def update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] + 1
        self.total_obs[a] = self.total_obs[a] + 1
        if self.debug:
            print "(n=%d, a=%d, ns=%d)-> %d/%d" % (self.index, a, ns,
                self.data[a][ns], self.total_obs[a])

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] - 1
        self.total_obs[a] = self.total_obs[a] - 1
