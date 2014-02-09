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
w = World(args.states, args.actions)
ssteps = steps = args.steps
step_points = [x for x in range(1, steps+1)]
prior = args.prior
alpha = args.alpha

strats = [RandomStrat(w, '-r', None, prior, alpha),
          UnembodiedStrat(w, '-k', None,  prior, alpha),
          PigGreedyStrat(w, 'g', None, prior, alpha),
          PigGreedyVIStrat(w, 'b', None, False, prior, alpha),
          PigGreedyVIStrat(w, 'm', None, True, prior, alpha)]
strats_data = [[] for i in range(len(strats))]

initial_mi = strats[0].compute_mi()

# Step through for all models
while steps > 0:
    msg = "("
    for i in range(len(strats)):
        mi = strats[i].compute_mi()
        strats_data[i].append(mi)
        msg += "%s_MI=%f " % (strats[i].name, mi)

        strats[i].step()

    msg += ")"

    if steps % (ssteps / 10) == 0:
        print msg
    steps = steps - 1

# Display text data for each model
w.display()
for strat in strats:
    strat.display()

# Generate Graphs
try:
    import matplotlib.pyplot as plt
except:
    print "\n***WARNING***\nUnable to generate graph. Please install matplotlib.\n***WARNING***"
    sys.exit(0)

plt.xlabel('Time (steps)', fontdict={'fontsize':16})
plt.ylabel('Missing Information (bits)', fontdict={'fontsize':16})
plt.title('1-2-3 Worlds [N=%d, M=%d]' % (args.states, args.actions))
plt.axis([0, ssteps, 0, initial_mi * 1.1])

for i in range(len(strats)):
    interval = 5
    plt.plot(step_points, strats_data[i], strats[i].color, label=strats[i].name)
    if strats[i].marker:
        plt.plot(step_points[0:len(step_points):interval],
              strats_data[i][0:len(step_points):interval],
              strats[i].marker, markersize=4, markerfacecolor='none')


plt.legend(bbox_to_anchor=(0.65, 0.85), loc=2, borderaxespad=0.)

plt.show()
