"""
    Runme to generate graphs for the Graph environment
"""

import string
import argparse
from graph import *
from runner import Runner
import config
import networkx as nx

from functions import *
import sys

class GraphRunner(Runner):

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.nodes = args.nodes
        self.connect = args.connect
        self.title = '[Graph, NRuns=%d]' % (self.runs)
        config.GRAPHICS = False # Not supported

    def setup_arguments(self):
        defaults = [200, 1]
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-n", "--nodes", dest="nodes", default=defaults[0],
                            type=int, help="Number of nodes (default: %d)" % defaults[0])
        parser.add_argument("-m", "--nodes_connect", dest="connect", default=defaults[1],
                            type=int, help="Nodes to connect to (default: %d)" % defaults[1])


        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        super(GraphRunner, self).setup_arguments(parser)
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        graph = nx.barabasi_albert_graph(self.nodes, self.connect)
        for i in range(config.RUNS):
            config.ENVIRON.append(Graph(graph))
        self.strats = config.init_strats()

def main():
    r = GraphRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())

