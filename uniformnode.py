import random
import math


class UniformNode:

    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.actions = []
        self.actions.append([])

        for action in range(M):
            self.actions.append([x for x in range(N)])

    def update(self, s1, s2):
        pass
        # TODO
