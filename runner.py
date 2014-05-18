"""
    This class implements all the general parts of running an environment. To
    generate graphs for environment run the corresponding runner that inherits
    this class, i.e. worldrunner.py, mazerunner.py, or denserunner.py
"""

import traceback
import pdb
import random
import string
import argparse
import numpy
from world import World
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from maze import *
from datetime import datetime as dt

from multiprocessing import Pool, Queue, Manager
import multiprocessing
import config

from functions import *
import sys

class Runner(object):

    def setup_arguments(self, parser):
        defaults = [config.STEPS, config.RUNS]
        parser.add_argument("-o", "--ofile", dest="ofile", default=None,
                            type=str, help="Name of file to output data to (default: None)")
        parser.add_argument("-i", "--ifile", dest="ifile", default=None,
                            type=str, help="Name of file to import data from (default: None")
        parser.add_argument('-v', dest="verbose", action='store_true',
                            help="Print extra info, e.g. the posterior")
        parser.add_argument('-d', dest="dump", action='store_true',
                            help="Dump the data to stdout")
        parser.add_argument('-c', dest="cluster", action='store_true',
                            help="Cluster mode, assert if config is incorrect.")
        parser.add_argument("-s", "--steps", dest="steps", default=defaults[0], type=int,
                          help="Number of steps to run (default: %d)" % defaults[0])
        parser.add_argument("-r", "--runs", dest="runs", default=defaults[1], type=int,
                          help="Number of runs to average over (default: %d)" %
                          defaults[1])
        parser.add_argument('-l', dest="lump", action='store_true',
                            help="Compare (PSI'+ ETA) with PSI instead of finifying")


        args = parser.parse_args()
        self.ofile   = args.ofile or config.EXPORT_FILE
        self.ifile   = args.ifile or config.IMPORT_FILE
        self.verbose = args.verbose
        self.dump    = args.dump or config.DUMP_STDOUT
        self.steps   = args.steps
        self.runs    = args.runs
        config.FINIFY = not args.lump

        self.elapsed = datetime.timedelta(0)
        self.nprocesses = multiprocessing.cpu_count()

        if args.cluster:
            assert config.DUMP_STDOUT
            assert not config.SERIAL
            assert not config.GRAPHICS

    # Records the Missing Information at each step for each strategy
    def init_strats_data(self):
        self.strats_data = [[] for i in range(len(self.strats))]
        for i in range(len(self.strats)):
            for s in range(self.steps):
                self.strats_data[i].append(0.0)

    # Run each strategy in parallel and aggregate the data together
    def collect_data(self):
        self.initial_mi = 0
        self.init_strats_data()

        self.strats_reward = [[] for i in range(len(self.strats))]

        start = dt.now()

        jobs = []
        strats = self.strats

        for i in range(len(strats)):
            self.initial_mi = max(self.initial_mi, strats[i].compute_mi())
            jobs += [i] * self.runs

        print "Running %d jobs" % len(jobs)

        if config.GRAPHICS or config.SERIAL:
            assert self.runs == 1
            strat_collect_serial(strats, self.strats_data, self.steps)
            return strats_data

        m = Manager()
        q = m.Queue()
        p = Pool(self.nprocesses)
        running = 0
        for j in range(self.nprocesses):
            if len(jobs) == 0:
                break
            i = jobs.pop()
            p.apply_async(strat_collect, args=(q, i, strats[i], self.steps))
            running += 1

        z = 0
        while running > 0:
            i, data, reward = q.get()

            print 'Job %d completed name=%s, elapsed=%ds' % (z, \
                            strats[i].get_name(), (dt.now() - start).seconds)
            sys.stdout.flush()
            z = z + 1

            for j in range(len(data)):
                self.strats_data[i][j] += data[j]
            self.strats_reward[i].append(reward)

            if len(jobs):
                i = jobs.pop()
                p.apply_async(strat_collect, args=(q, i, strats[i], self.steps))
            else:
                running -= 1 # Didn't start another job to replace this one

        p.close()
        p.join()

        self.elapsed = dt.now() - start

    # Average the Missing Information, run stats on reward
    def analyze_data(self):
        for i in range(len(self.strats)):
            for s in range(self.steps):
                self.strats_data[i][s] /= self.runs
            arr = numpy.array(self.strats_reward[i])
            print 'ARR',arr
            self.strats_reward[i] = [numpy.mean(arr), numpy.std(arr)]

    def graph_data(self):
        try:
            import matplotlib.pyplot as plt
        except:
            print """\n***WARNING***\nUnable to generate graph.
                 Please install matplotlib. \n***WARNING***"""
            sys.exit(0)
        print "Graphing data..."

        mi_height = self.initial_mi
        step_points = [i for i in range(self.steps)]
        plt.xlabel('Time (steps)', fontdict={'fontsize':16})
        plt.ylabel('Missing Information (bits)', fontdict={'fontsize':16})
        plt.title(self.title + " Elapsed=%ds) " % self.elapsed.seconds)
        plt.axis([0, self.steps, 0, mi_height * 1.1])


        for i in range(len(self.strats)):
            mi = self.strats_data[i][self.steps - 1]
            plt.plot(step_points, self.strats_data[i],
                     #color=self.strats[i].color,
                     label=self.strats[i].get_name() + "MI=" + str(mi))

        plt.legend(bbox_to_anchor=(0,0.8), loc=2, borderaxespad=0.)
        plt.show()

    def export_data(self, f):
        for i in range(len(self.strats_data)):
            for s in range(len(self.strats_data[i])):
                f.write('%f ' % self.strats_data[i][s])
            f.write('\n')

        f.write('Summary\n')
        for i in range(len(self.strats_data)):
            f.write('%s ' % self.strats[i].get_name())
            mi = self.strats_data[i][self.steps - 1]
            f.write('MI=%f ' % mi)
            [m, std] = self.strats_reward[i]
            f.write('Mean Reward=%f (std=%f)\n' % (m, std))


    def import_data(self):
        f = open(self.ifile, 'r')
        strats_data = []
        l = f.readline()
        i = 0
        initial_mi = 0
        while l != '' and l != '\n':
            if l.startswith('Elap') or l.startswith('Run') or \
                    l.startswith('Job'):# skip progress lines
                l = f.readline()
                continue
            if l.startswith('Summary'):
                break

            strats_data.append([])
            step = 0
            for mi in l.split():
                mi = float(mi)
                if not initial_mi:
                    initial_mi = mi
                strats_data[i].append(mi)
                step = step + 1

            self.steps = step

            i = i + 1
            l = f.readline()

        self.initial_mi = initial_mi
        return strats_data

    def run(self):
        if self.ifile:
            strats_data = self.import_data()
        else:
            self.collect_data()
            self.analyze_data()

            # Display text representation of Model
            if self.verbose:
                config.ENVIRON.display()
                for i in range(len(self.strats)):
                    self.strats[i].display()

            if self.ofile:
                self.export_data(open(self.ifile, 'r'))
            if self.dump:
                self.export_data(sys.stdout)
                return # done

        self.graph_data(strats_data)

def strat_collect_serial(strats, strats_data, steps):
    step = 0
    mi = 0
    while step < steps:
        i = 0
        for strat in strats:
            mi = strat.compute_mi()
            strats_data[i][step] = mi
            strat.step(step, mi)
            i += 1

        # Monitor progress at subjob level
        if steps < 10 or step % (steps / 10) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        step = step + 1

def strat_collect(q, i, strat, steps):
    try:
        step = 0
        mi = 0
        strats_data = [0 for j in range(steps)]
        while step < steps:
            mi = strat.compute_mi()

            strats_data[step] = mi
            strat.step(step, mi)

            #raise Exception("Hi") # Test

            # Monitor progress at subjob level
            #if steps < 10 or step % (steps / 10) == 0:
                #sys.stdout.write('.')
                #sys.stdout.flush()

            step = step + 1
        reward = strat.get_reward()
        q.put((i, strats_data, reward))
    except Exception as e:
        traceback.print_exc()
        print 'e', e.value
        q.put((i, e))
    return -1
