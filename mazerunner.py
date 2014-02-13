"""
    Runme to generate graphs for the 123World environment
"""

import string
from optparse import OptionParser
import argparse
from world import World
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from piggreedyvistrat import *
from maze import *
from runner import Runner

from functions import *
import sys

class MazeRunner(Runner):
    # Setup arguments for controlling states, actions, steps, etc.

    # Strategies used in this run
    def init_strats(self):
        return [
                RandomStrat(self.maze, Dirichlet(self.maze), '-r'),
                UnembodiedStrat(self.maze, Dirichlet(self.maze), '-k'),
                PigGreedyStrat(self.maze, Dirichlet(self.maze), 'g'),
                PigGreedyVIStrat(self.maze, Dirichlet(self.maze), 'b', False),
                PigGreedyVIStrat(self.maze, Dirichlet(self.maze), 'm', True)
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = args.mazef
        self.steps   = args.steps
        self.runs    = args.runs
        self.ofile   = args.ofile
        self.ifile   = args.ifile
        self.verbose = args.verbose
        self.title = '[Maze N=36 States, M=4 Actions, R=%d Runs]' % self.runs

    def setup_arguments(self):
        defaults = ['maze.txt', 300, 5]

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-m", "--mazef", dest="mazef", default=defaults[0],
                            type=str, help="""txt file to generate maze from (default: %s)""" % defaults[0])
        parser.add_argument("-s", "--steps", dest="steps", default=defaults[1], type=int,
                          help="Number of steps to run (default: %d)" % defaults[1])
        parser.add_argument("-r", "--runs", dest="runs", default=defaults[2], type=int,
                          help="Number of runs to average over (default: %d)" %
                          defaults[2])
        parser.add_argument("-o", "--ofile", dest="ofile", default=None,
                            type=str, help="Name of file to output data to (default: None)")
        parser.add_argument("-i", "--ifile", dest="ifile", default=None,
                            type=str, help="Name of file to graph data from (default: None")
        parser.add_argument("-v", "--verbose", dest="verbose", default=False, type=bool,
                          help="Print more information (unsupported at the moment)")
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        self.maze = Maze(self.mazef)
        self.strats = self.init_strats()


def main():
    r = MazeRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
