"""
    An unembodied agent explores the world without limitation on a position. It
    picks a (a,s) that maximizes its PIG

    Notes
    - MultiProcess results in a ~30% performance gain with 4 CPUs on 123World
"""

import random
from dirichlet import Dirichlet
from functions import *
from bayesworld import *
import datetime

from multiprocessing import Process, Pool
import multiprocessing

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

    # Look for the (state, action) pair that results in the most pig and then
    # take it. This is pretty slow...
    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return

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
            p.apply_async(subset_max_gain, args=(self.im, start, end),
                          callback=global_max_gain)
        p.close()
        p.join()

        ns = self.tm.take_action(best_s, best_a)
        self.im.update(best_a, best_s, ns)
        self.pos = ns

    def display(self):
        self.im.display(self.name)

# Compute the max gain for a subset of states i.e. those from *start* to *stop*
# Each process is assigned a subset
def subset_max_gain(im, start, stop):
    max_gain, best_a, best_s = (-1.0, -1, -1)
    for s in range(start, stop):
        for a in range(im.M):
            pig = predicted_information_gain(im, a, s)
            if pig > max_gain:
                max_gain, best_a, best_s = (pig, a, s)
    return (max_gain, best_a, best_s)
