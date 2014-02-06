"""
    Runme to generate graphs of different exploration strategies
"""

import string
from optparse import OptionParser
import argparse
from world import World
from stratrandom import StratRandom
from stratunembodied import StratUnembodied
from functions import *
import sys

levels = [[5,3,50],
          [10,3,100],
          [20,3,1000]]
msgs = []
for n in range(len(levels)):
    msgs.append("(%d) - N=%d, M=%d, S=%d" % (n+1, levels[n][0], levels[n][1],
                    levels[n][2]))


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-l", "--level", dest="level", default=0, type=int,
                  help='Run at a certain complexity level.\n%s\n%s\n%s\nUsing this argument overrides all other options.'
                       % (msgs[0], msgs[1], msgs[2]))
parser.add_argument("-n", "--states", dest="states", default=10, type=int,
                  help="Number of unique states")
parser.add_argument("-m", "--actions", dest="actions", default=3, type=int,
                  help="Number of unique actions")
parser.add_argument("-s", "--steps", dest="steps", default=100, type=int,
                  help="Number of steps to run")
parser.add_argument("-v", "--verbose", dest="verbose", default=False, type=bool,
                  help="Print more information (unsupported at the moment)")
args = parser.parse_args()

if args.level:
    l = args.level - 1
    w = World(levels[l][0], levels[l][1])
    ssteps = steps = levels[l][2]
else:
    w = World(args.states, args.actions)
    ssteps = steps = args.steps
step_points = [x for x in range(1, steps+1)]

sr = StratRandom(w)
sr_data = []

su = StratUnembodied(w)
su_data = []

initial_mi = sr.compute_mi()

while steps > 0:
    sr_mi = sr.compute_mi()
    sr_data.append(sr_mi)
    sr.step()

    su_mi = su.compute_mi()
    su_data.append(su_mi)
    su.step()

    if steps % (ssteps / 10) == 0:
        print "(Random_MI=%f, Unembodied_MI=%f)" % (sr_mi, su_mi)
    steps = steps - 1

w.display()
sr.display()
su.display()

try:
    import matplotlib.pyplot as plt
    plt.xlabel('Time (steps)')
    plt.ylabel('Missing Information (bits)')
    plt.title('1-2-3 Worlds [N=%d, M=%d]' % (args.states, args.actions))
    plt.axis([0, ssteps, 0, initial_mi * 1.1])

    base_x = ssteps * 0.75
    text_x = ssteps * 0.82
    base_y = initial_mi * 0.9
    text_y = initial_mi * 0.885
    diff_y = initial_mi * 0.05
    plt.text(base_x, base_y, '____')
    plt.text(text_x, text_y, 'Unembodied')

    plt.text(base_x, base_y - diff_y, '____', color='red')
    plt.text(text_x, text_y - diff_y, 'Random')

    plt.plot(step_points, sr_data, '-r,')
    plt.plot(step_points, su_data, '-k')
    plt.show()
except:
    print "\n***WARNING***\nUnable to generate graph. Please install matplotlib.\n***WARNING***"

