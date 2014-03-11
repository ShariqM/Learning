"""
    Runme to generate graphs for the Maze environment
"""

import string
import argparse
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from pigvistrat import *
from maze import *
from runner import Runner
from dirichletp import DirichletProcess

from functions import *
import sys

class MazeRunner(Runner):

    # Strategies used in this run
    def init_strats(self):
        return [
                RandomStrat(self.maze, Dirichlet(self.maze), '-r'),
                UnembodiedStrat(self.maze, Dirichlet(self.maze), '-k'),
                PigGreedyStrat(self.maze, Dirichlet(self.maze), 0, 'g'),
                PigGreedyStrat(self.maze, DirichletProcess(self.maze), 1, '-c'),
                #PigVIStrat(self.maze, Dirichlet(self.maze), 0, 'b', False),
                #PigVIStrat(self.maze, DirichletProcess(self.maze), 1, 'y', False),
                #PigVIStrat(self.maze, Dirichlet(self.maze), 0, 'm', True)
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = "maze_files/%s" % args.mazef
        self.steps   = args.steps
        self.runs    = args.runs
        self.title = '[Maze F=%s, R=%d Runs]' % (self.mazef, self.runs)

    def setup_arguments(self):
        defaults = ['maze.txt', 300, 5]

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-m", "--mazef", dest="mazef", default=defaults[0],
                            type=str, help="""Read this .txt file from maze_files/ to generate the maze default: %s)""" % defaults[0])
        parser.add_argument("-s", "--steps", dest="steps", default=defaults[1], type=int,
                          help="Number of steps to run (default: %d)" % defaults[1])
        parser.add_argument("-r", "--runs", dest="runs", default=defaults[2], type=int,
                          help="Number of runs to average over (default: %d)" %
                          defaults[2])

        super(MazeRunner, self).setup_arguments(parser)
        return parser.parse_args()

    def __init__(self):
        self.init_variables()
        self.maze = Maze(self.mazef)
        self.environ = self.maze # So Runner can specify any environ
        self.strats = self.init_strats()

def main():
    r = MazeRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
