"""
    Runme to generate graphs for the Chain environment
"""

import string
import argparse
from maze import *
from maze3d import *
from runner import Runner
import config

from functions import *
import sys

class Chainunner(Runner):

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = "maze_files/%s" % args.mazef
        self.steps   = args.steps
        self.runs    = args.runs
        self.title = '[Maze File=%s, NRuns=%d]' % (args.mazef, self.runs)
        config.GRAPHICS = args.graphics or config.GRAPHICS
        config.FINIFY = not args.lump

    def setup_arguments(self):
        defaults = [config.MAZE, config.STEPS, config.RUNS, config.GRAPHICS]

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-m", "--mazef", dest="mazef", default=defaults[0],
                            type=str, help="""Read this .txt file from maze_files/ to generate the maze default: %s)""" % defaults[0])
        parser.add_argument("-s", "--steps", dest="steps", default=defaults[1], type=int,
                          help="Number of steps to run (default: %d)" % defaults[1])
        parser.add_argument("-r", "--runs", dest="runs", default=defaults[2], type=int,
                          help="Number of runs to average over (default: %d)" %
                          defaults[2])
        parser.add_argument('-g', dest="graphics", action='store_true',
                            help="Toggle visualization")
        parser.add_argument('-l', dest="lump", action='store_true',
                            help="Compare (PSI'+ ETA) with PSI instead of finifying")

        super(MazeRunner, self).setup_arguments(parser)
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        if '3d' in self.mazef:
            config.ENVIRON = Maze3d(self.mazef)
        else:
            config.ENVIRON = Maze(self.mazef)
        self.strats = config.init_strats()

def main():
    r = MazeRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())

