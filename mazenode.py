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
            #print dist
            #dist = [round(x, 2) for x in dist]
            #print dist
            highest = 0.0
            tgt_i = '0'
            for i in range(4):
                if dist[i] > highest:
                    highest = dist[i]
                    tgt_i = i
            # Align the highest probability with the action index
            tmp = dist[a]
            dist[a] = highest
            dist[tgt_i] = tmp
            self.actions.append(dist)

    def get_prob(self, a, ns):
        if ns not in self.neighbors:
            return 0.0
        for j in range(4):
            if self.neighbors[j] == ns:
                return round(self.actions[a][j], 3)

    def take_action(self, a):
        return self.neighbors[sample(self.actions[a])]
