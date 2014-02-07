"""
FIXME
    A dirichlet node calculates probability of entering a new node based on it's
    data. Its data is updated everytime it enters a new state.
"""

import random
import math
from functions import *

class BayesWorldNode:

    def __init__(self, M, N, index, debug=False):
        self.M = M
        self.N = N
        self.T = [0 for i in range(self.M)] # Number of target states observed for action a
        self.index = index
        self.actions = []
        self.data = []
        self.total_obs = []
        self.debug = debug

        for action in range(M):
            self.data.append([0 for x in range(N)])
            self.total_obs.append(0)
            self.actions.append([x for x in range(N)])

    def get_prob_help(self, a, ns):
        if self.data[a][ns]: # previously observed
            return 1 / (a + 1.0)
        if self.T[a] == a + 1: # all transitions found.
            return 0.0 # Necessary to avoid (1 choose 2) (not in paper)

        if self.data[a][0]:
            return (1 - (self.T[a]/(a + 1.0))) / (self.N - self.T[a])

        if ns == 0:
            num = 1.0 - math.pow(0.75, a+1)
            den = 1.0 + (choose(a, self.T[a]) - 1) * math.pow(0.75, a+1)
            return (1/(a+1.0)) * (num / den)
        else:
            x = self.get_prob(a, 0)
            num = 1.0 - (self.T[a]/(a + 1.0) + self.get_prob(a, 0))
            return num / (self.N - self.T[a] - 1.0)

    def get_prob(self, a, ns):
        r = self.get_prob_help(a, ns)
        return r if r > 0 else 0.0

    def get_sprob(self, a, ns):
        return "(%d/%d)" % (self.data[a][ns] + 1, self.total_obs[a] + self.N)

    def update(self, a, ns):
        if not self.data[a][ns]:
            self.T[a] = self.T[a] + 1
            #print "gained a T"
        else:
            #print "didn't gain a T"
            pass
        self.data[a][ns] += 1

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.T[a] -= 1
            if self.T[a] < 0:
                raise Exception("FOO!")
        self.data[a][ns] -= 1
