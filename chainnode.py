"""
    A Chain node determines the probability of entering new node given an action
"""

import math
import numpy.random as ran
import config
from functions import *

class ChainNode:

    def __init__(self, M, neighbors):
        self.neighbors = neighbors # Neighboring states
        self.M = M
        self.actions = [[0.2, 0.8], [0.8, 0.2]] # The distribution of actions

    def get_prob(self, a, ns, new_states=None):
        if ns == config.PSI and new_states:
            unk_prob = 0.0
            for ns in set(self.neighbors):
                if ns in new_states:
                    continue
                unk_prob += self.get_prob(a, ns)
            return unk_prob

        if ns not in self.neighbors:
            return 0.0

        for j in range(self.M):
            if self.neighbors[j] == ns:
                return self.actions[a][j]

    def get_neighbors(self):
        return self.neighbors

    def take_action(self, a):
        return self.neighbors[sample(self.actions[a])]
