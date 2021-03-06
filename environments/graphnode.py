"""
    A World node determines the probability of entering new node given an action
"""

import math
import numpy.random as ran
import config
import random
from functions import *

class GraphNode:

    def __init__(self, neighbors):
        self.neighbors = neighbors # Neighboring states
        self.actions = [] # The distribution of each action
        self.M = len(neighbors)

        for a in range(self.M):
            if config.DETERMINISTIC:
                dist = [0] * a + [1] + [0] * (self.M - a - 1) # Generate prob=1 for a
            elif random.random() < 0.5:
                dist = ran.dirichlet([1.0/self.M] * self.M) # Uniform alpha's
                dist = realign(self.M, a, dist)
            else:
                dist = [1.0/self.M] * self.M

            self.actions.append(dist)

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

        tsum = 0.0
        for j in range(self.M):
            if self.neighbors[j] == ns:
                # we may have 2 neighbors that point to self
                #tsum += round(self.actions[a][j], 5)
                tsum += self.actions[a][j]
        return tsum

    def get_neighbors(self):
        return set(self.neighbors)

    def take_action(self, a):
        return self.neighbors[sample(self.actions[a])]

# Place the highest probability in position a
def realign(M, a, dist):
    highest = -1.0
    high_i = -1
    for i in range(M):
        if dist[i] > highest:
            highest = dist[i]
            high_i = i

    # Swap dist[a] with dist[high_i]
    tmp = dist[a]
    dist[a] = highest
    dist[high_i] = tmp

    return dist
