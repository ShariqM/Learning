"""
    A prior dirichlet distribution that is going to
    move towards a real model through bayesian updates.
"""

from dirichletnode import DirichletNode
import random

class Dirichlet(object):

    def __init__(self, tm):
        self.N = tm.N
        self.M = tm.M
        # Start with a uniform distribution
        self.nodes = [DirichletNode(self.M, self.N, i) for i in range(self.N)]
        self.mid = random.random()
        self.moves = 0

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        self.moves = self.moves + 1
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        self.moves = self.moves - 1
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        i = 1
        print "*** %s Dirichlet (Internal) Model ***" % strat
        for node in self.nodes:
            print "\t%d."% i
            ia = 0
            for a in node.actions:
                print "\t\t(%d)-->" % ia, ["%.2f" % node.get_prob(ia, ns) for ns in
                    range(self.N)]
                #print "\t\t(%d)-->" % ia, [node.get_sprob(ia, ns) for ns in
                    #range(self.N)]
                ia = ia + 1
            print "\n\n"
            i = i + 1

    def is_affected_by(self, a, s):
        return False
