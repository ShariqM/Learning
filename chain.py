"""
    5-state "Chain" Problem from Sterns 2000
"""

from functions import *
from chainnode import ChainNode
from model import Model
import config

class Chain(Model):

    def __init__(self):
        self.N = 5
        self.M = 2
        self.nodes = []
        for i in range(self.N):
            nextnode = i + (1 if i != self.N - 1 else 0)
            reward = [0 if i != self.N - 1 else 1, 0.2]
            self.nodes.append(ChainNode(self.M, [0, nextnode], reward))

    def take_action(self, s, a):
        return self.nodes[s].take_action(a)

    def get_prob(self, a, s, ns, new_states=None):
        return self.nodes[s].get_prob(a, ns, new_states)

    def get_neighbors(self, s):
        return self.nodes[s].get_neighbors()

    def display(self):
        print "*** Chain (Real) Model ***"
        super(Maze, self).display()
