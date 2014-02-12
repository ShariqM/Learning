"""
    A DirichletNode encodes the internal probability distribution model for a
    single node. Bayesian updates described in section (1) and (2) of Appendix A2.
"""

import random
import math

class DirichletNode:

    def __init__(self, M, N, index, is_maze, debug=False):
        self.M = M
        self.N = N
        self.index = index
        self.actions = []
        self.data = []
        self.total_obs = []
        self.debug = debug
        self.is_maze = is_maze
        self.alpha = 0.25 if is_maze else 1.0

        for action in range(M):
            self.data.append([0 for x in range(N)])
            self.total_obs.append(0)
            self.actions.append([x for x in range(N)])

    # Dirichlet distribution with alpha=0.25 (Equation 14)
    def get_prob_maze(self, a, ns):
        Ns = 4
        osum = 0
        for os in range(self.M):
            osum += self.data[a][os]
        return (self.data[a][ns] + self.alpha) / (Ns * self.alpha + osum)

    def get_prob(self, a, ns):
        if self.is_maze:
            return self.get_prob_maze(a, ns)
        # Dirichlet distribution with alpha=1 (Equation 13)
        return (self.alpha + self.data[a][ns]) / (self.total_obs[a] + self.N*self.alpha)

    def update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] + 1
        self.total_obs[a] = self.total_obs[a] + 1

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        self.data[a][ns] = self.data[a][ns] - 1
        self.total_obs[a] = self.total_obs[a] - 1
