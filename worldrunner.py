"""
    Runme to generate graphs for the 123World environment
"""

import string
import argparse
from world import World
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from pigvistrat import *
from maze import *
from runner import Runner

from functions import *
import sys

class WorldRunner(Runner):
    # Setup arguments for controlling states, actions, steps, etc.

    # Strategies used in this run
    def init_strats(self):
        return [
                RandomStrat(self.world, BayesWorld(self.world), '-r'),
                UnembodiedStrat(self.world, BayesWorld(self.world), '-k'),
                PigGreedyStrat(self.world, BayesWorld(self.world), 'g'),
                PigVIStrat(self.world, BayesWorld(self.world), 'b', False),
                PigVIStrat(self.world, BayesWorld(self.world), 'm', True)
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()

        if args.level: # Override M, N, S
            l = args.level - 1
            args.states = self.levels[l][0]
            args.actions = self.levels[l][1]
            args.steps = self.levels[l][2]

        self.states  = args.states
        self.actions = args.actions
        self.steps   = args.steps
        self.runs    = args.runs
        self.title = '1-2-3 Worlds [N=%d States, M=%d Actions, R=%d Runs]' % \
                        (self.states, self.actions, self.runs)

    def setup_arguments(self):
        defaults = [10,3,100]
        self.levels = [[3,3,200],
                       [7,3,400],
                       [10,3,500],
                       [20,3,1000]]
        levels = self.levels
        msgs = ["(0) - Use values from -n, -m, -s"]
        for n in range(len(levels)):
            msgs.append("(%d) - N=%d, M=%d, S=%d" % (n+1, levels[n][0], levels[n][1],
                            levels[n][2]))

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-l", "--level", dest="level", default=0, type=int,
                          help='Run at a certain complexity level.\n%s\n%s\n%s\n%s\n%s\nUsing this argument overrides all other options. (default: 0)'
                               % (msgs[0], msgs[1], msgs[2], msgs[3], msgs[4]))
        parser.add_argument("-n", "--states", dest="states", default=defaults[0], type=int,
                          help="Number of unique states (default: %d)" % defaults[0])
        parser.add_argument("-m", "--actions", dest="actions", default=defaults[1], type=int,
                          help="Number of unique actions (default: %d)" % defaults[1])
        parser.add_argument("-s", "--steps", dest="steps", default=defaults[2], type=int,
                          help="Number of steps to run (default: %d)" % defaults[2])
        parser.add_argument("-r", "--runs", dest="runs", default=5, type=int,
                          help="Number of runs to average over")

        super(WorldRunner, self).setup_arguments(parser)

        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        self.world = World(self.states, self.actions)
        self.environ = self.world
        self.strats = self.init_strats()


def main():
    r = WorldRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
