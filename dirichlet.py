"""
    An internal, prior distribution model to learn the real Maze and DenseWorld
    distribution's.
"""

from dirichletnode import DirichletNode
from bayesworldnode import BayesWorldNode
import random

class Dirichlet(object):

    def __init__(self, tm):
        self.N = tm.N
        self.M = tm.M
        self.nodes = [DirichletNode(self.M, self.N, get_neighbors(tm, i),
                                    tm.is_maze()) for i in range(self.N)]

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        i = 1
        print "*** %s Dirichlet (Internal) Model ***" % strat
        for node in self.nodes:
            print "\t%d."% i
            ia = 0
            for a in node.actions:
                arr = []
                for ns in range(self.N):
                    if node.get_prob(ia, ns) <= 0.0:
                        continue
                    arr.append((ns, round(node.get_prob(ia, ns), 3)))
                print "\t\t(a=%d)-->" % ia,  arr
                ia = ia + 1
            print "\n\n"
            i = i + 1

    def is_affected_by(self, a, s):
        return False

def get_neighbors(tm, i):
    if not tm.is_maze():
        return []
    return tm.get_neighbors(i)
