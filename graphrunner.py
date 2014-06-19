"""
    Runme to generate graphs for the Graph environment
"""

import string
import argparse
from graph import *
from runner import Runner
import config

from functions import *
import sys

class GraphRunner(Runner):

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.title = '[Graph, NRuns=%d]' % (self.runs)
        config.GRAPHICS = False # Not supported

    def setup_arguments(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        super(GraphRunner, self).setup_arguments(parser)
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        for i in range(config.RUNS):
            config.ENVIRON.append(Graph())
        self.strats = config.init_strats()

def main():
    r = GraphRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())

