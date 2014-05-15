"""
    Runme to generate graphs for the Maze environment
"""

import string
import argparse
from maze import *
from maze3d import *
from runner import Runner
import config

from functions import *
import sys

class MazeRunner(Runner):

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = "maze_files/%s" % args.mazef
        self.title = '[Maze File=%s, NRuns=%d]' % (args.mazef, self.runs)
        config.GRAPHICS = args.graphics or config.GRAPHICS

    def setup_arguments(self):
        defaults = [config.MAZE]

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-m", "--mazef", dest="mazef", default=defaults[0],
                            type=str, help="""Read this .txt file from maze_files/ to generate the maze default: %s)""" % defaults[0])
        parser.add_argument('-g', dest="graphics", action='store_true',
                            help="Toggle visualization")

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
