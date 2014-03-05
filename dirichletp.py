"""
    An internal, prior distribution model to learn the real Maze distribution.
    Modeled off the Dirichlet Process or Chinese Restaurant Process
"""

from dirichletpnode import DirichletProcessNode
from model import Model
import random

class DirichletProcess(Model):

    def __init__(self, tm):
        self.M = tm.M
        self.nodes = {}
        self.nodes[0] = DirichletProcessNode(self.M)

    def get_neighbors(self, s, a):
        return self.nodes[s].get_neighbors(a)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        print "*** %s Dirichlet (Internal) Model ***" % strat
        super(Dirichlet, self).display()
