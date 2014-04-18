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
from ltavistrat import *
from maze import *
from runner import Runner
from dirichletp import DirichletProcess
import config

from functions import *
import sys

colors = {
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

ALPHA=3.0
DEFAULT_MAZE='maze.mz'
DEFAULT_STEPS=300
DEFAULT_RUNS=5
DEFAULT_GRAPHICS=False

#strats = {
    #(strat="PigVi", model="CRP a=1.0",
#}kk

# Strategy
#

class MazeRunner(Runner):

    # Strategies used in this run
    def init_strats(self):
        i = 0
        return [
         #RandomStrat(self.maze, Dirichlet(self.maze), colors['red']),
         #RandomStrat(self.maze, DirichletProcess(self.maze), colors['red2']),
         #UnembodiedStrat(self.maze, Dirichlet(self.maze), colors['black']),
         #UnembodiedStrat(self.maze, DirichletProcess(self.maze), colors['grey']),
         #PigGreedyStrat(self.maze, Dirichlet(self.maze), colors['blue']),
         #PigGreedyStrat(self.maze, DirichletProcess(self.maze), colors['grue2']),
         #PigVIStrat(self.maze, Dirichlet(self.maze), colors['green'], 0),

         #PigVIStrat(self.maze, DirichletProcess(self.maze, 0.01), colors['red'], 0),
         #PigVIStrat(self.maze, DirichletProcess(self.maze, 0.25), colors['blue'], 0),
         PigVIStrat(self.maze,
                    DirichletProcess(self.maze, ALPHA),
                    colors['red'], plus=0, explorer=True),
         PigVIStrat(self.maze,
                    DirichletProcess(self.maze, ALPHA),
                    colors['blue'], plus=0, explorer=False),
         #PigVIStrat(self.maze, DirichletProcess(self.maze, ALPHA), colors['blue'],
                    #0, False, True),
         #PigVIStrat(self.maze, DirichletProcess(self.maze, 4.0), colors['green'], 0),
         #PigVIStrat(self.maze, DirichletProcess(self.maze, 25.0), colors['yellow'], 0),
         #PigVIStrat(self.maze, DirichletProcess(self.maze, 100.0), colors['purple'], 0),

         #PigVIStrat(self.maze, Dirichlet(self.maze), colors['blue'], 1),
         #PigVIStrat(self.maze, DirichletProcess(self.maze), colors['blue2'], 1),
         #LTAStrat(self.maze, DirichletProcess(self.maze), colors['yellow'])
         #LTAStrat(self.maze, Dirichlet(self.maze), colors['yellow']),
         #LTAVIStrat(self.maze, Dirichlet(self.maze), colors['purple3'])
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()
        self.mazef   = "maze_files/%s" % args.mazef
        self.steps   = args.steps
        self.runs    = args.runs
        self.title = '[Maze F=%s, R=%d Runs]' % (self.mazef, self.runs)
        config.GRAPHICS = args.graphics
        config.FINIFY = not args.lump

    def setup_arguments(self):
        defaults = [DEFAULT_MAZE, DEFAULT_STEPS, DEFAULT_RUNS, DEFAULT_GRAPHICS]

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
        self.maze = Maze(self.mazef)
        self.environ = self.maze # So Runner can specify any environ
        self.strats = self.init_strats()

def main():
    r = MazeRunner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
