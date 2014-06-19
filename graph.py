"""
    Graph represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

import string
import sys
from functions import *
from graphnode import GraphNode
from model import Model
import config
import random
import math
import networkx as nx


class Graph(Model):

    def __init__(self, graph):
        self.graph = graph
        self.N = self.graph.number_of_nodes()
        self.nodes = []

        for neighbors in self.graph.adjacency_list():
            print 's', len(self.nodes), neighbors
            self.nodes.append(GraphNode(neighbors))

    def take_action(self, s, a):
        ns = self.nodes[s].take_action(a)
        return ns, 0

    def get_prob(self, a, s, ns, new_states=None):
        return self.nodes[s].get_prob(a, ns, new_states)

    def get_num_actions(self, s):
        if s == config.ETA or s == config.PSI:
            return 4 # Doesn't matter (happens on hypothetical)
        return self.nodes[s].M

    def get_neighbors(self, s):
        return self.nodes[s].get_neighbors()

    def display(self):
        print "*** Graph (Real) Model ***"
        super(Graph, self).display()
