"""
    An internal, prior distribution model to learn the real Maze and DenseWorld
    distribution's.
"""

from dirichletnode import DirichletNode
from bayesworldnode import BayesWorldNode
from model import Model
import random

class Dirichlet(Model):

    def __init__(self, tm, alpha=0.25):
        self.N = tm.N
        self.M = tm.M
        self.nodes = [DirichletNode(self.M, self.N, alpha, tm.get_neighbors(i))
                                    for i in range(self.N)]
        self.alpha = alpha

    def get_name(self):
        return "D [a=%.2f]" % self.alpha

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns, r=0):
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        print "*** %s Dirichlet (Internal) Model ***" % strat
        super(Dirichlet, self).display()
