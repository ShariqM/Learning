"""
    Runme to generate graphs for the Maze environment
"""

import string
import argparse
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from pigvistrat import *
from ltastrat import *
from maze import *
from runner import Runner
from dirichletp import DirichletProcess

from functions import *
import sys

colors = {
"""
b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white
    {'c': (0.0, 0.75, 0.75), 'b': (0.0, 0.0, 1.0), 'w': (1.0, 1.0, 1.0), 'g':
    (0.0, 0.5, 0.0), 'y': (0.75, 0.75, 0), 'k': (0.0, 0.0, 0.0), 'r': (1.0, 0.0,
    0.0), 'm': (0.75, 0, 0.75)}
    """
          'red'     : (1.0, 0.0, 0.0), # Red
          'red2'    : (0.7, 0.2, 0.2),
          'red3'    : (0.3, 0.1, 0.1),
          'green'   : (0.0, 1.0, 0.0), # Green
          'green2'  : (0.2, 0.7, 0.2),
          'green3'  : (0.1, 0.3, 0.1),
          'blue'    : (0.0, 0.0, 1.0), # Blue
          'blue2'   : (0.2, 0.2, 0.7),
          'blue3'   : (0.1, 0.1, 0.3),
          'yellow'  : (1.0, 1.0, 0.0),
          'yellow2' : (0.7, 0.7, 2.0),
          'yellow3' : (0.3, 0.3, 1.0),
          'grue'    : (0.0, 1.0, 1.0),
          'grue2'   : (0.2, 0.7, 0.7), # cyan
          'grue3'   : (0.1, 0.3, 0.3),
          'purple'  : (1.0, 0.0, 1.0),
          'purple2' : (0.7, 0.2, 0.7),
          'purple3' : (0.3, 0.1, 0.3),
          'black'   : (0.0, 0.0, 0.0),
          'grey'    : (0.2, 0.2, 0.2),
         }

class MazeRunner(Runner):

    # Strategies used in this run
    def init_strats(self):
        i = 0
        return [
         #RandomStrat(self.maze, Dirichlet(self.maze), colors['red']),
         RandomStrat(self.maze, DirichletProcess(self.maze), colors['red2']),
         #UnembodiedStrat(self.maze, Dirichlet(self.maze), colors['black']),
         UnembodiedStrat(self.maze, DirichletProcess(self.maze), colors['grey']),
         #PigGreedyStrat(self.maze, Dirichlet(self.maze), colors['blue']),
         PigGreedyStrat(self.maze, DirichletProcess(self.maze), colors['grue2']),
         #PigVIStrat(self.maze, Dirichlet(self.maze), colors['green'], 0),
         PigVIStrat(self.maze, DirichletProcess(self.maze), colors['green2'], 0),
         #PigVIStrat(self.maze, Dirichlet(self.maze), colors['blue'], 1),
         PigVIStrat(self.maze, DirichletProcess(self.maze), colors['blue2'], 1),
         LTAStrat(self.maze, DirichletProcess(self.maze), colors['yellow'])
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = "maze_files/%s" % args.mazef
        self.steps   = args.steps
        self.runs    = args.runs
        self.title = '[Maze F=%s, R=%d Runs]' % (self.mazef, self.runs)

    def setup_arguments(self):
        defaults = ['maze.mz', 300, 5]

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

def inc(i):
    i = i + 1
    return i - 1
