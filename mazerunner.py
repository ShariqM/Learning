"""
    Runme to generate graphs of different exploration strategies
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

from functions import *
import sys

# Setup arguments for controlling states, actions, steps
defaults = [10,3,100]
levels = [[3,3,200],
          [10,3,300],
          [20,3,1000]]
msgs = ["(0) - Use values from -n, -m, -s"]
for n in range(len(levels)):
    msgs.append("(%d) - N=%d, M=%d, S=%d" % (n+1, levels[n][0], levels[n][1],
                    levels[n][2]))


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-l", "--level", dest="level", default=0, type=int,
                  help='Run at a certain complexity level.\n%s\n%s\n%s\n%s\nUsing this argument overrides all other options. (default: 0)'
                       % (msgs[0], msgs[1], msgs[2], msgs[3]))
parser.add_argument("-n", "--states", dest="states", default=defaults[0], type=int,
                  help="Number of unique states (default: %d)" % defaults[0])
parser.add_argument("-m", "--actions", dest="actions", default=defaults[1], type=int,
                  help="Number of unique actions (default: %d)" % defaults[1])
parser.add_argument("-s", "--steps", dest="steps", default=defaults[2], type=int,
                  help="Number of steps to run (default: %d)" % defaults[2])
parser.add_argument("-a", "--alpha", dest="alpha", default=1.0, type=float,
                  help="Alpha value for Dirichlet distribution (default: 1.0)")
parser.add_argument("-p", "--prior", dest="prior", default=0, type=int,
                  help="Prior Distribution\n(0) - Bayes specific to 123World\n(1) - Dirichlet distribution\n (default: 0)")
parser.add_argument("-v", "--verbose", dest="verbose", default=False, type=bool,
                  help="Print more information (unsupported at the moment)")
args = parser.parse_args()

# Initialize world according to arguments
if args.level: # Override M, N, S
    l = args.level - 1
    args.states = levels[l][0]
    args.actions = levels[l][1]
    args.steps = levels[l][2]

m = Maze('maze.txt')

