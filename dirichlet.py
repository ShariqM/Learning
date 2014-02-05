"""
    A prior dirichlet distribution that is going to
    move towards a real model through bayesian updates.
"""

from dirichletnode import DirichletNode

class Dirichlet:

    def __init__(self, tm):
        self.N = tm.N
        self.M = tm.M
        # Start with a uniform distribution
        self.nodes = [DirichletNode(self.M, self.N, i) for i in range(self.N)]

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        return self.nodes[s].update(a, ns)

    def display(self):
        i = 1
        print "*** Dirichlet (Internal) Model ***"
        for node in self.nodes:
            print "\t%d."% i
            ia = 0
            for a in node.actions:
                print "\t\t(%d)-->" % ia, [node.get_prob(ia, ns) for ns in
                range(self.N)]
                ia = ia + 1
            print "\n\n"
            i = i + 1
