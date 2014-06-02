"""
    An internal, prior distribution model to learn the real Maze distribution.
    Modeled off the Dirichlet Process or Chinese Restaurant Process
"""

from gampypnode import GamPypProcessNode
from ifunctions import *
import random
import sys
import config

class GamPypProcess(object):

    def __init__(self, tm, theta=0.001, KA=0.25, finify_by=2.0):
        self.M = tm.M
        self.nodes = {}
        self.theta = theta
        self.KA = KA
        self.nodes[config.SS] = GamPypProcessNode(self.M, self.theta, self.KA)
        self.last_update = config.NULL_UPDATE
        self.total_reward = 0.0
        assert type(finify_by) != int
        self.finify_by = finify_by
        self.information_gain = 0.0

    def get_information_gain(self):
        return self.information_gain

    def get_finify_by(self):
        return self.finify_by

    def get_abbr(self):
        return "GAMPYP"

    def get_name(self):
        return "GamPyp [T=%.3f, KA=%.3f, f=%f]" % \
                    (self.theta, self.KA, self.finify_by)

    def get_known_states(self, a=config.NULL_ARG, s=config.NULL_ARG):
        if s == config.NULL_ARG:
            return self.nodes.keys()
        return self.nodes[s].get_states(a)

    def get_states(self, a=config.NULL_ARG, s=config.NULL_ARG):
        states = self.get_known_states(a, s)
        if config.PSI in states:
            raise "State Corruption"
        return states + [config.PSI]

    def has_state(self, s):
        return self.nodes.has_key(s)

    def is_aware_of(self, a, s, ns):
        return self.nodes[s].is_aware_of(a, ns)

    def get_prob_first_obs(self):
        return self.nodes[config.SS].get_prob_first_obs()

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    def get_reward(self, a, s):
        if s == config.PSI:
            return 0
            #return config.MAX_REWARD
        if a not in range(self.M):
            raise Exception("Invalid action")
        return self.nodes[s].get_reward(a)

    def update_information(self, a, s, ns):
        new_state = not self.nodes[s].is_aware_of(a, ns)
        self.information_gain += information_gain(self, a, s, ns, new_state)

    # Update model given the data
    def update(self, a, s, ns, r=0):
        new_state = not self.nodes.has_key(ns)
        if new_state:
            self.last_update = ns
            self.nodes[ns]   = GamPypProcessNode(self.M, self.theta, self.KA)
        else:
            self.last_update = config.NULL_UPDATE

        self.total_reward += r
        return self.nodes[s].update(a, ns, r)

    # Undo update (for hypothetical updates)
    def undo_update(self, a, s, ns):
        if self.last_update != config.NULL_UPDATE:
            self.nodes.pop(self.last_update)
        return self.nodes[s].undo_update(a, ns)

    def display(self, strat):
        pr("*** %s GamPyp Process (Internal) Model ***" % strat)
        pr("a=Action, s=Starting State, ns=New state, p=Probability")
        pr("For each (s,a) we display a list of (ns, p), the p of entering ns")
        for i, node in self.nodes.items():
            pr("\tFrom Starting State=%d." % i)
            for a in range(node.M):
                arr = []
                new_states = self.get_states(a, i)
                for ns in new_states:
                    if node.get_prob(a, ns) <= 0.0:
                        continue
                    arr.append((ns, round(node.get_prob(a, ns), 3)))
                r = self.get_reward(a, i)
                pr("\t\t(s=%d, a=%d) [r=%f] ->" % (i, a, r) + str(arr))
            pr("")

        if True:
            for i, node in self.nodes.items():
                pr("\tFrom Starting State=%d." % i)
                node.stats()
                pr('\n')
        sys.stdout.flush()

    def has_unknown_states(self):
        return True

def pr(s):
    sys.stdout.write(s+'\n')
    sys.stdout.flush()
