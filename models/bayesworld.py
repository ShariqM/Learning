"""
    An internal, prior distribution model to learn the real 123World distribution.
"""

from bayesworldnode import BayesWorldNode
from model import Model
import random

class BayesWorld(Model):

    def __init__(self, tm):
        self.N = tm.N
        self.M = tm.M
        self.nodes = [BayesWorldNode(self.M, self.N, i) for i in range(self.N)]

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        print "*** %s BayesWorld (Internal) Model ***" % strat
        super(BayesWorld, self).display()
