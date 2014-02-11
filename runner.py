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

class Runner():

    # Setup arguments for controlling states, actions, steps, etc.
    def setup_arguments(self):
        defaults = [10,3,100]
        self.levels = [[3,3,200],
                       [10,3,300],
                       [20,3,1000]]
        levels = self.levels
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
        return parser.parse_args()

    # Strategies used in this run
    def init_strats(self):
        return [RandomStrat(self.world, '-r', None, self.prior, self.alpha),
                UnembodiedStrat(self.world, '-k', None,  self.prior, self.alpha),
                PigGreedyStrat(self.world, 'g', None, self.prior, self.alpha),
                #PigGreedyVIStrat(self.world, 'b', None, False, self.prior, self.alpha),
                #PigGreedyVIStrat(self.world, 'm', None, True, self.prior, self.alpha)
               ]

    # Initialize variables according to arguments
    def init_variables(self):
        args = self.setup_arguments()

        if args.level: # Override M, N, S
            l = args.level - 1
            args.states = self.levels[l][0]
            args.actions = self.levels[l][1]
            args.steps = self.levels[l][2]

        self.states  = args.states
        self.actions = args.actions
        self.steps   = args.steps
        self.prior   = args.prior
        self.alpha   = args.alpha
        self.runs    = 1
        self.verbose = args.verbose

    def __init__(self):
        self.init_variables()
        self.world = World(self.states, self.actions)
        self.strats = self.init_strats()

    def init_strats_data(self):
        strats_data = [[] for i in range(len(self.strats))]
        for i in range(len(self.strats)):
            strats_data.append([])
            for s in range(self.steps):
                strats_data[i].append(0.0)
        return strats_data

    def print_msg(step):
        # Maybe later
        #msg = "\t(Step=%d, " % step
        #msg += "%s_MI=%f " % (strats[i].name, mi)
        pass

    def collect_data(self):
        # Missing information for each step of each strat
        strats_data = self.init_strats_data()

        run = 0
        while run < self.runs:
            print "Run %d " % run,
            strats = self.init_strats()
            self.initial_mi = strats[0].compute_mi()

            step = 0
            while step < self.steps:
                for i in range(len(strats)):
                    strats_data[i][step] += strats[i].compute_mi()
                    strats[i].step()
                step = step + 1
                if step % (self.steps / 10) == 0:
                    sys.stdout.write('.')
                sys.stdout.flush()
            run = run + 1
            print ''
        return strats_data

    # Average the data and find when MI hits 0
    def analyze_data(self, strats_data):
        strats_finish = [0 for i in range(len(self.strats))]
        for i in range(len(self.strats)):
            for s in range(self.steps):
                strats_data[i][s] /= self.runs
                if (strats_data[i][s] <= 0.0 or s == self.steps -1) and \
                    not strats_finish[i]:
                    strats_finish[i] = s
        return strats_data, strats_finish

    def graph_data(self, strats_data, strats_finish):
        # Generate Graphs
        try:
            import matplotlib.pyplot as plt
            from scipy.interpolate import spline
            import numpy as np
            import scipy
        except:
            print """\n***WARNING***\nUnable to generate graph.
                 Please install matplotlib, scipy, and numpy. \n***WARNING***"""
            sys.exit(0)

        step_points = [i for i in range(self.steps)]
        plt.xlabel('Time (steps)', fontdict={'fontsize':16})
        plt.ylabel('Missing Information (bits)', fontdict={'fontsize':16})
        plt.title('1-2-3 Worlds [N=%d, M=%d]' % (self.states, self.actions))
        plt.axis([0, self.steps, 0, self.initial_mi * 1.1])

        for i in range(len(self.strats)):
            weights = self.get_weights(strats_finish[i])
            z2 = np.polyfit(step_points, strats_data[i], 2, w=weights)
            p2 = np.poly1d(z2)
            #xnew = np.linspace(0, min(steps, steps * 1.5), steps * 20)
            xnew = np.linspace(0, min(self.steps, strats_finish[i]), self.steps * 20)
            plt.plot(xnew, p2(xnew), self.strats[i].color, label=self.strats[i].name)

            plt.plot(step_points, strats_data[i], self.strats[i].color,
                     label=self.strats[i].name)

            #xnew = np.linspace(0, steps, steps * 20)
            #smooth = spline(step_points, strats_data[i], xnew)
            #plt.plot(xnew, smooth, strats[i].color, label=strats[i].name)
            if self.strats[i].marker:
                interval = 5
                plt.plot(step_points[0:len(step_points):interval],
                      strats_data[i][0:len(step_points):interval],
                      self.strats[i].marker, markersize=4, markerfacecolor='none')

        plt.legend(bbox_to_anchor=(0.65, 0.85), loc=2, borderaxespad=0.)
        plt.show()

    def run(self):
        strats_data = self.collect_data()
        strats_data, strats_finish = self.analyze_data(strats_data)
        self.graph_data(strats_data, strats_finish)

    def get_weights(self, stop):
        weights = [i < stop for i in range(self.steps)] # 1 before stop, 0 after
        weights[0] = weights[i] = self.steps / 10 # weight the end points by alot
        return weights

def main():
    r = Runner()
    r.run()

if __name__ == "__main__":
    sys.exit(main())
