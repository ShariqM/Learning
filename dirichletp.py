"""
    An internal, prior distribution model to learn the real Maze distribution.
    Modeled off the Dirichlet Process or Chinese Restaurant Process
"""

from dirichletpnode import DirichletProcessNode
import random

NULL_UPDATE = -9999

class DirichletProcess(object):

    def __init__(self, tm):
        self.M = tm.M
        self.nodes = {}
        self.nodes[0] = DirichletProcessNode(self.M)
        self.last_update = NULL_UPDATE

    def get_name(self):
        return "DirichP"

    def get_known_states(self, a=-5, s=-5):
        if s == -5:
            return self.nodes.keys()
        return self.nodes[s].get_states(a)

    def get_states(self, a=-5, s=-5):
        states = self.get_known_states(a, s)
        # -1 represents the Unknown state
        if -1 in states: #Think about this
            raise "State Corruption"
        return states + [-1]

    def has_state(self, s):
        return self.nodes.has_key(s)

    def is_aware_of(self, a, s, ns):
        return self.nodes[s].is_aware_of(a, ns)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    # Update model given the data
    def update(self, a, s, ns):
        if not self.nodes.has_key(ns):
            self.last_update = ns
            self.nodes[ns] = DirichletProcessNode(self.M)
        else:
            self.last_update = NULL_UPDATE
        return self.nodes[s].update(a, ns)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        if self.last_update != NULL_UPDATE:
            self.nodes.pop(self.last_update)
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        print "*** %s Dirichlet Process (Internal) Model ***" % strat
        print "a=Action, s=Starting State, ns=New state, p=Probability"
        print "For each (s,a) we display a list of (ns, p), the p of entering ns"
        for i, node in self.nodes.items():
            print "\tFrom Starting State=%d."% i
            for a in range(node.M):
                arr = []
                new_states = self.get_states(a, i) + [-1]
                for ns in new_states:
                    if node.get_prob(a, ns) <= 0.0:
                        continue
                    arr.append((ns, round(node.get_prob(a, ns), 3)))
                print "\t\t(s=%d, a=%d) ->" % (i, a),  arr
            print ""
        #super(Dirichlet, self).display()

    def has_unknown_states(self):
        return True
