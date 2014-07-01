"""
    Runme to generate graphs for the Chain environment
"""

import string
import argparse
from environments.chain import *
from runner import Runner
import config

from functions import *
import sys

class ChainRunner(Runner):

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.title = '[Chain, NRuns=%d]' % (self.runs)
        config.GRAPHICS = False

    def setup_arguments(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        super(ChainRunner, self).setup_arguments(parser)
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        for i in range(config.RUNS):
            config.ENVIRON.append(Chain())
        self.strats = config.init_strats()

def main():
    r = ChainRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
