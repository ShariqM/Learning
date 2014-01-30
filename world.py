"""
    123World represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. For example, it keeps to state about a user of the environment.
"""

from worldnode import WorldNode

class World:

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.nodes = [WorldNode(M, N) for i in range(self.N)]

    def take_action(self, s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    def display(self):
        i = 1
        print "*** 123World (Real) Model ***"
        for node in self.nodes:
            print "------%d-------" % i
            ia = 0
            for a in node.actions:
                print "\t(%d)-->" % ia, a
                ia = ia + 1
            print "\n\n"
            i = i + 1
