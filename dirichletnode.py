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
        self.data = []
        self.obs_num = []
        self.total_obs = []
        self.neighbors = neighbors
        # In the paper we knew the # of neighbors, we are moving away from this.
        # self.Ns = len(set(self.neighbors)) # Number of unique neighbors
        self.Ns = self.N
        self.alpha = 0.25

        for action in range(M):
            self.data.append([0 for x in range(N)])
            self.obs_num.append(0)
            self.total_obs.append(0)

    # Dirichlet distribution with alpha=0.25 (Equation 14)
    def get_prob(self, a, ns):
        # See note above about neighbors
        #if ns not in self.neighbors:
            #return 0.0

        return (self.data[a][ns] + self.alpha) /  \
            (self.Ns * self.alpha + self.obs_num[a])

    def update(self, a, ns):
        self.data[a][ns]  = self.data[a][ns]  + 1
        self.obs_num[a]   = self.obs_num[a]   + 1
        self.total_obs[a] = self.total_obs[a] + 1

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        self.data[a][ns]  = self.data[a][ns]  - 1
        self.obs_num[a]   = self.obs_num[a]   - 1
        self.total_obs[a] = self.total_obs[a] - 1
