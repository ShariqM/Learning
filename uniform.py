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

    # Do I need this ?
    def take_action(s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def display(self):
        i = 1
        for node in self.nodes:
            print "------%d-------" % i
            ia = 0
            for a in node.actions:
                print "\t(%d)-->" % ia, a
                ia = ia + 1
            print "\n\n"
            i = i + 1
