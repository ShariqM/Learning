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
import time
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

PAUSER = True

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
                self.strats_data[i].append([])

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
            jobs += [(i,j) for j in range(self.runs)]

        print "Running %d jobs" % len(jobs)

        if config.GRAPHICS or config.SERIAL:
            assert self.runs == 1
            strat_collect_serial(strats, self.strats_data,
                                self.strats_reward, self.steps)
            return

        m = Manager()
        q = m.Queue()
        p = Pool(self.nprocesses)
        running = 0
        for j in range(self.nprocesses):
            if len(jobs) == 0:
                break
            i,j = jobs.pop()
            strats[i].update_tm(config.ENVIRON[j])
            p.apply_async(strat_collect, args=(q, i, strats[i], self.steps))
            running += 1

        z = 0
        while running > 0:
            i, data, reward = q.get()

            print 'Job %d completed name=%s, elapsed=%ds' % (z, \
                            strats[i].get_name(), (dt.now() - start).seconds)
            sys.stdout.flush()
            z = z + 1

            for s in range(len(data)):
                self.strats_data[i][s].append(data[s])
            self.strats_reward[i].append(reward)

            if len(jobs):
                i,j = jobs.pop()
                strats[i].update_tm(config.ENVIRON[j])
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
                length = len(self.strats_data[i][s])

                mi_arr = [self.strats_data[i][s][j][0] for j in range(length)]
                mi_arr = numpy.array(mi_arr)
                mi_mean, mi_std = numpy.mean(mi_arr), numpy.std(mi_arr)

                ns_arr = [self.strats_data[i][s][j][1] for j in range(length)]
                ns_arr = numpy.array(ns_arr)
                ns_mean, ns_std = numpy.mean(ns_arr), numpy.std(ns_arr)

                self.strats_data[i][s] = [(mi_mean, mi_std), (ns_mean, ns_std)]
            arr = numpy.array(self.strats_reward[i])
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
        plt.xlabel('Time (steps)', fontdict={'fontsize':24})
        plt.ylabel('Missing Information (bits)', fontdict={'fontsize':24})
        plt.title("Maze", fontsize=26)
        #plt.title(self.title + " Elapsed=%ds) " % self.elapsed.seconds)
        plt.axis([0, self.steps, 2700, mi_height * 1.01])


        for i in range(len(self.strats)):
            #mi = self.strats_data[i][self.steps - 1][0][0]
            mean_data = [data[0][0] - 0 for data in self.strats_data[i]]
            plt.plot(step_points, mean_data,
                     color=self.strats[i].color,
                     #label=self.strats[i].get_sname() + " MI=" + str(mi))
                     linewidth=1.5,
                     #label=self.strats[i].get_name())
                     label=self.strats[i].get_sname())


        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        lg = plt.legend(fontsize=20)
        lg.draw_frame(False)

        #plt.legend(bbox_to_anchor=(0.8 , 1.00), loc=2,
                   #fontsize=20)
        plt.show()

        ns_height = 150
        step_points = [i for i in range(self.steps)]
        plt.xlabel('Time (steps)', fontdict={'fontsize':24})
        plt.ylabel('States Discovered', fontdict={'fontsize':24})
        #plt.ylabel('Missing Information (bits)', fontdict={'fontsize':24})
        plt.title("Maze", fontsize=26)
        #plt.title(self.title + " Elapsed=%ds) " % self.elapsed.seconds)
        plt.axis([0, self.steps, 0, ns_height * 1.1])


        for i in range(len(self.strats)):
            #mi = self.strats_data[i][self.steps - 1][1][0]
            mean_data = [data[1][0] - 0 for data in self.strats_data[i]]
            plt.plot(step_points, mean_data,
                     color=self.strats[i].color,
                     #label=self.strats[i].get_sname() + " MI=" + str(mi))
                     linewidth=1.5,
                     #label=self.strats[i].get_name())
                     label=self.strats[i].get_sname())


        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        lg = plt.legend(fontsize=20)
        lg.draw_frame(False)

        #plt.legend(bbox_to_anchor=(0.8 , 1.00), loc=2,
                   #fontsize=20)
        plt.show()



    def export_data(self, f):
        for i in range(len(self.strats_data)):
            for s in range(len(self.strats_data[i])):
                #FIXME
                f.write('%f %d ' % (self.strats_data[i][s][0][0],
                                   self.strats_data[i][s][1][0]))
            f.write('\n')

        f.write('Summary\n')
        for i in range(len(self.strats_data)):
            f.write('%s ' % self.strats[i].get_name())
            mi = self.strats_data[i][self.steps - 1][0]
            f.write('Mean MI=%f (std=%f) | ' % (mi[0], mi[1]))

            ns = self.strats_data[i][self.steps - 1][1]
            f.write('Mean NS=%f (std=%f) | ' % (ns[0], ns[1]))

            [m, std] = self.strats_reward[i]
            f.write('Mean Reward=%f (std=%f)\n' % (m, std))

    def import_data(self):
        f = open(self.ifile, 'r')
        self.strats_data = []
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

            self.strats_data.append([])
            step = 0
            mi_turn = True
            last_mi = -1
            for value in l.split():
                if mi_turn:
                    last_mi = float(value)
                    if not initial_mi:
                        initial_mi = last_mi
                    mi_turn = False
                else:
                    ns = float(value)
                    mi_turn = True
                    self.strats_data[i].append([(last_mi, 0), (ns, 0)]) #FIXME
                    step = step + 1

            self.steps = step

            i = i + 1
            l = f.readline()

        self.initial_mi = initial_mi

    def run(self):
        if self.ifile:
            self.import_data()
        else:
            self.collect_data()
            self.analyze_data()

            # Display text representation of Model
            if self.verbose:
                config.ENVIRON[0].display()
                for i in range(len(self.strats)):
                    self.strats[i].display()

            if self.ofile:
                self.export_data(open(self.ifile, 'r'))
            if self.dump:
                self.export_data(sys.stdout)
                return # done

        self.graph_data()

def strat_collect_serial(strats, strats_data, strats_reward, steps):
    step = 0
    mi = 0
    while step < steps:
        i = 0
        for strat in strats:
            mi = strat.compute_mi()
            #mi = strat.get_information_gain()
            #print 'ig', mi
            strats_data[i][step] = mi
            strat.step(step, mi)
            i += 1

        if PAUSER and step % 500 == 0:
            time.sleep(5)

        # Monitor progress at subjob level
        if steps < 10 or step % (steps / 10) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()


        step = step + 1

    for i in range(len(strats)):
        strats_reward[i] = strats[i].get_reward()


def strat_collect(q, i, strat, steps):
    try:
        step = 0
        mi = 0
        strats_data = [0 for j in range(steps)]
        while step < steps:
            mi = strat.compute_mi()
            nstates = len(strat.im.get_known_states())
            #mi = strat.get_information_gain()

            strats_data[step] = (mi, nstates)
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
