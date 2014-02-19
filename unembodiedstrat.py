"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG

    Notes
    - MultiProcess results in a
        - ~30% performance gain with 4 CPUs on 123World
        - ~100% performance gain with 4 CPUs on Maze
    - There is no concurrency control so we are assuming concurrent PIG
      computations are independent. This is true for 123World since updating
      one (stage, action) does not affect another other (state, action)
"""

import random
from dirichlet import Dirichlet
from functions import *
from bayesworld import *
import datetime
import pdb

from multiprocessing import Pool
import multiprocessing

# Compute the max gain for a subset of states i.e. those from *start* to *stop*
# Each process is assigned a subset
#def subset_max_gain(im, start, stop):
#def subset_max_gain(start, stop):
    #return (1,1,1)
def subset_max_gain(im, start, stop):
    max_gain, best_a, best_s = (-1.0, -1, -1)
    for s in range(start, stop):
        for a in range(im.M):
            pig = predicted_information_gain(im, a, s)
            if pig > max_gain:
                max_gain, best_a, best_s = (pig, a, s)
    return (max_gain, best_a, best_s)

class UnembodiedStrat():

    def __init__(self, tm, im, color, marker=None):
        self.tm = tm
        self.im = im
        self.name = "Unembodied"
        self.color = color
        self.marker = marker

        # Multiprocess organization
        self.nprocesses = multiprocessing.cpu_count()
        self.state_division = [] # describes which states go to which process
        remainder = self.tm.N % self.nprocesses # remainder states
        states_pp = self.tm.N / self.nprocesses # states per process
        end = 0
        for i in range(self.nprocesses):
            start = end
            end = end + states_pp + (1 if remainder > 0 else 0)
            remainder -= 1
            self.state_division.append((start,end))

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def step_serial(self):
        max_gain, best_a, best_s = (-1.0, -1, -1)
        for s in range(self.im.N):
            for a in range(self.im.M):
                pig = predicted_information_gain(self.im, a, s)
                if pig > max_gain:
                    max_gain, best_a, best_s = (pig, a, s)
        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
        self.pos = ns
        return


    # Look for the (state, action) pair that results in the most pig and then
    # take it. This is pretty slow...
    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return

        serial = False
        if serial:
            return self.step_serial()

        tstart = datetime.datetime.now()
        global max_gain, best_a, best_s
        max_gain, best_a, best_s = (-1.0, -1, -1)

        # compute the max gain of the subset max gains
        def global_max_gain(state_tuple):
            gain, a, s = state_tuple
            global max_gain, best_a, best_s
            if gain > max_gain:
                max_gain, best_a, best_s = (gain, a, s)

        p = Pool(self.nprocesses) # Pool of processes
        for i in range(self.nprocesses):
            start, end = self.state_division[i]
            #print start, end
            #p.apply_async(subset_max_gain, args=(self.im, start, end))
            #p.apply_async(subset_max_gain, args=(start, end))
            p.apply_async(subset_max_gain, args=(self.im, start, end),
                          callback=global_max_gain)
        p.close()
        p.join()

        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
        self.pos = ns
        #print "time = ", (datetime.datetime.now() - tstart).microseconds

    def display(self):
        self.im.display(self.name)


