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

    def __init__(self):
        self.graph = nx.barabasi_albert_graph(10, 2)
        self.N = self.graph.number_of_nodes()
        self.nodes = []
        self.rnodes = []

        for neighbors in self.graph.adjacency_list();
            self.nodes.append(GraphNode(self.M, neighbors))

    def take_action(self, s, a):
        ns = self.nodes[s].take_action(a)
        return ns, self.rnodes[ns]

    def get_prob(self, a, s, ns, new_states=None):
        return self.nodes[s].get_prob(a, ns, new_states)

    def get_num_actions(self, s):
        return self.nodes[s].M

    def get_neighbors(self, s):
        return self.nodes[s].get_neighbors()

    def display(self):
        print "*** Graph (Real) Model ***"
        super(Graph, self).display()
