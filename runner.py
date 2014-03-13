"""
    This class implements all the general parts of running an environment. To
    generate graphs for environment run the corresponding runner that inherits
    this class, i.e. worldrunner.py, mazerunner.py, or denserunner.py
"""

import string
import argparse
from world import World
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from maze import *

from multiprocessing import Pool, Queue, Manager
import multiprocessing

from functions import *
import sys

class Runner(object):

    def setup_arguments(self, parser):
        parser.add_argument("-o", "--ofile", dest="ofile", default=None,
                            type=str, help="Name of file to output data to (default: None)")
        parser.add_argument("-i", "--ifile", dest="ifile", default=None,
                            type=str, help="Name of file to import data from (default: None")
        parser.add_argument('-v', dest="verbose", action='store_true',
                            help="Print extra info, e.g. the posterior")
        parser.add_argument('-d', dest="dump", action='store_true',
                            help="Dump the data to stdout")

        args = parser.parse_args()
        self.ofile   = args.ofile
        self.ifile   = args.ifile
        self.verbose = args.verbose
        self.dump    = args.dump
        self.elapsed = datetime.timedelta(0)
        self.nprocesses = multiprocessing.cpu_count()

    def init_strats_data(self):
        strats_data = [[] for i in range(len(self.strats))]
        for i in range(len(self.strats)):
            strats_data.append([])
            for s in range(self.steps):
                strats_data[i].append(0.0)
        return strats_data

        # Step through each strategy, record the MI at each step
    def collect_data(self):
        # Missing information for each step of each strat
        global strats_data
        strats_data = self.init_strats_data()
        self.initial_mi = 0
        start = datetime.datetime.now()

        jobs = []
        self.strats = strats = self.init_strats()
        for i in range(len(strats)):
            self.initial_mi = max(self.initial_mi, strats[i].compute_mi())
            jobs += [i] * self.runs

        print "Running %d jobs" % len(jobs)

        def collect_data(i):
            def collect_data_i(data):
                for j in range(len(data)):
                    strats_data[i][j] += data[j]
            return collect_data_i

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
            i, data = q.get()
            print 'Job %d completed' % z
            z = z + 1
            for j in range(len(data)):
                strats_data[i][j] += data[j]
            if len(jobs):
                i = jobs.pop()
                p.apply_async(strat_collect, args=(q, i, strats[i], self.steps))
            else:
                running -= 1

        #p = Pool(self.nprocesses)
        #i,j = (0,0)
        #while i < self.nprocess and j < len(jobs):
            #p.apply_async(strat_collect, args=(strats[i], self.steps),
                          #callback=collect_data(i))
        p.close()
        p.join()

        self.elapsed = datetime.datetime.now() - start
        return strats_data

    # Average the data and find when MI hits 0
    def analyze_data(self, strats_data):
        for i in range(len(self.strats)):
            for s in range(self.steps):
                strats_data[i][s] /= self.runs
        return strats_data

    def graph_data(self, strats_data):
        try:
            import matplotlib.pyplot as plt
        except:
            print """\n***WARNING***\nUnable to generate graph.
                 Please install matplotlib. \n***WARNING***"""
            sys.exit(0)
        print "Graphing data..."

        step_points = [i for i in range(self.steps)]
        plt.xlabel('Time (steps)', fontdict={'fontsize':16})
        plt.ylabel('Missing Information (bits)', fontdict={'fontsize':16})
        plt.title(self.title + " Elapsed=%ds) " % self.elapsed.seconds)
        plt.axis([0, self.steps, 0, self.initial_mi * 1.1])

        for i in range(len(self.strats)):
            plt.plot(step_points, strats_data[i],
                     color=self.strats[i].color,
                     label=self.strats[i].get_name())

        plt.legend(bbox_to_anchor=(0.8,1), loc=2, borderaxespad=0.)
        plt.show()

    def export_data(self, strats_data, f):
        for i in range(len(strats_data)):
            for s in range(len(strats_data[i])):
                f.write('%f ' % strats_data[i][s])
            f.write('\n')

    def import_data(self):
        f = open(self.ifile, 'r')
        strats_data = []
        l = f.readline()
        i = 0
        initial_mi = 0
        while l != '' and l != '\n':
            if l.startswith('Elap'):# skip progress lines
                l = f.readline()
                continue

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
            strats_data = self.collect_data()
            strats_data = self.analyze_data(strats_data)

            # Display text representation of Model
            if self.verbose:
                self.environ.display()
                for i in range(len(self.strats)):
                    if i == 0:
                        continue
                    self.strats[i].display()

            if self.ofile:
                self.export_data(strats_data, open(self.ifile, 'r'))
            if self.dump:
                self.export_data(strats_data, sys.stdout)
                return

        self.graph_data(strats_data)

def strat_collect(q, i, strat, steps):
    try:
        step = 0
        mi = 0
        strats_data = [0 for j in range(steps)]
        while step < steps:
            mi = strat.compute_mi()
            strats_data[step] += mi
            strat.step(mi)

            step = step + 1
            #if steps < 10 or step % (steps / 10) == 0:
                #sys.stdout.write('.')
                #sys.stdout.flush()
        q.put((i, strats_data))
    except Exception as e:
        print 'e', e
        return e
    return -1
