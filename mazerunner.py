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
                #RandomStrat(self.maze, Dirichlet(self.maze), (1,0,0)),
                RandomStrat(self.maze, DirichletProcess(self.maze), (0.7,0.7,0)),
                #UnembodiedStrat(self.maze, Dirichlet(self.maze), (0,0,0)),
                UnembodiedStrat(self.maze, DirichletProcess(self.maze), (0.3,0.3,0.3)),
                #PigGreedyStrat(self.maze, Dirichlet(self.maze), (0,1,0)),
                #PigGreedyStrat(self.maze, DirichletProcess(self.maze), (0,0.7,0.7)),
                #PigVIStrat(self.maze, Dirichlet(self.maze), (0,0,1) , False),
                PigVIStrat(self.maze, DirichletProcess(self.maze), (0.7, 0, 0.7), False),
                #PigVIStrat(self.maze, Dirichlet(self.maze), (0.3, 0.8, 0.3), True),
                PigVIStrat(self.maze, DirichletProcess(self.maze), (0.2, 0.8, 0.5), True)
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
