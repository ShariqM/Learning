"""
    123World represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

from worldnode import WorldNode
from model import Model

class World(Model):

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.nodes = [WorldNode(M, N) for i in range(self.N)]

    def take_action(self, s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    def get_neighbors(self, s):
        return []

    def display(self):
        print "*** 123World (Real) Model ***"
        super(World, self).display()
