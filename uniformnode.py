import random
import math


class UniformNode:

    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.actions = []
        self.has_data = []

        for action in range(M):
            self.actions.append([x for x in range(N)])
            self.has_data.append(False)

    def get_prob(self, a, ns):
        dests = self.actions[a]
        return 1.0 / len(dests) if ns in dests else 0

    def update(self, a, ns):
        if not self.has_data[a]:
            self.actions[a] = [ns]
            self.has_data[a] = True
        elif ns not in self.actions[a]:
            self.actions[a].append(ns)
