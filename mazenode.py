"""
    A World node determines the probability of entering new node given an action
"""

import math
import numpy.random as random
from functions import *

class MazeNode:

    def __init__(self, neighbors):
        self.neighbors = neighbors # Neighboring states
        self.actions = [] # The distribution of each action

        for a in range(4):
            dist = random.dirichlet([0.25, 0.25, 0.25, 0.25]) # alpha = 0.25
            highest = 0.0
            for i in range(4):
                highest = max(highest, dist[i])
            # Align the highest probability with the action index
            tmp = dist[a]
            dist[a] = highest
            dist[(a+1)%4] = tmp
            self.actions.append(dist)
            print "a=%d, dist=" % a, dist

    def get_prob(self, a, ns):
        return 1.0 / (a+1) if ns in self.actions[a] else 0

    def take_action(self, a):
        return self.neighbors[sample(self.actions[a])]


