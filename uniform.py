"""
    A prior uniform distribution that is going to
    move towards a real model through bayesian updates.
"""

from uniformnode import UniformNode

class Uniform:

    def __init__(self, tm):
        self.N = tm.N
        self.M = tm.M
        # Assume a uniform distribution...
        self.nodes = [UniformNode(self.M, self.N) for i in range(self.N)]

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        return self.nodes[s].update(a, ns)

    def display(self):
        i = 1
        print "*** Uniform (Internal) Model ***"
        for node in self.nodes:
            print "\t%d."% i
            ia = 0
            for a in node.actions:
                print "\t\t(%d)-->" % ia, a
                ia = ia + 1
            print "\n\n"
            i = i + 1
