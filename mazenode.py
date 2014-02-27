"""
    A World node determines the probability of entering new node given an action
"""

import math
import numpy.random as ran
from functions import *

class MazeNode:

    def __init__(self, neighbors):
        self.neighbors = neighbors # Neighboring states
        self.actions = [] # The distribution of each action

        for a in range(4):
            dist = ran.dirichlet([0.25, 0.25, 0.25, 0.25]) # alpha = 0.25
            dist = realign(a, dist)
            self.actions.append(dist)

    def get_prob(self, a, ns):
        if ns not in self.neighbors:
            return 0.0

        tsum = 0.0
        for j in range(4):
            if self.neighbors[j] == ns:
                # we may have 2 neighbors that point to self
                tsum += round(self.actions[a][j], 3)
        return tsum

    def get_neighbors(self):
        return self.neighbors

    def take_action(self, a):
        return self.neighbors[sample(self.actions[a])]

# Place the highest probability in position a
def realign(a, dist):
    highest = -1.0
    high_i = -1
    for i in range(4):
        if dist[i] > highest:
            highest = dist[i]
            high_i = i

    # Swap dist[a] with dist[high_i]
    tmp = dist[a]
    dist[a] = highest
    dist[high_i] = tmp

    return dist
