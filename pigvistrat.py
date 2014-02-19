"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *

from multiprocessing import Pool
import multiprocessing

def subset_pigs(im, start, stop):
    data = []
    for a in range(im.M):
        data.append([])
        for s in range(start, stop):
            data[a].append(predicted_information_gain(im, a, s))
    return (start, stop, data)

class PigVIStrat():

    def __init__(self, tm, im, color, control=False, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(VI+)" if control else "PIG(VI)"
        self.color = color
        self.marker = marker
        self.plan = []
        self.plansteps = 5 # Number of steps to look in the future
        self.discount = 0.95 # Discount factor for gains in future
        self.control = control # VI+ if True (uses real model)

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

    def best_value(self, future, s):
        tmax = -1
        for a in range(self.im.M):
            if future[a][s] > tmax:
                tmax = future[a][s]
        return tmax

    def future_gain(self, i, all_futures, a, s):
        if i == 0:
            return 0

        tsum = 0
        for ns in range(self.im.N):
            m = self.tm if self.control else self.im
            tsum += m.get_prob(a, s, ns)  * self.best_value(all_futures[i-1], ns)

        return self.discount * tsum

    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return
        if len(self.plan) != 0:
            ns = self.tm.take_action(self.pos, self.plan[0])
            self.im.update(best_a, self.pos, ns)
            self.pos = ns
            return

        global pigs
        pigs = []
        for a in range(self.im.M):
            pigs.append([])
            for s in range(self.im.N):
                pigs[a].append(0)

        # Fill in the global pigs table
        def global_pigs(state_tuple):
            start, stop, data = state_tuple
            global pigs
            for s in range(start, stop):
                for a in range(self.im.M):
                    pigs[a][s] = data[a][s-start]

        p = Pool(self.nprocesses) # Pool of processes
        for i in range(self.nprocesses):
            start, end = self.state_division[i]
            p.apply_async(subset_pigs, args=(self.im, start, end),
                          callback=global_pigs)
        p.close()
        p.join()

        all_futures = [] # List of Q's from the paper
        for i in range(self.plansteps):
            all_futures.append([])
            for a in range(self.im.M):
                all_futures[i].append([])
                for s in range(self.im.N):
                    all_futures[i][a].append([])
                    all_futures[i][a][s] = pigs[a][s] + \
                        self.future_gain(i, all_futures, a, s)

        max_fgain = -1
        best_a = -1
        future = all_futures[self.plansteps - 1]
        for a in range(self.im.M):
            if future[a][self.pos] > max_fgain:
                max_fgain = future[a][self.pos]
                best_a = a

        #print "(a=%d, s=%d) pig=%d l=%d" % (best_a, self.pos, max_gain, \
                    #len(best_as))
        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

    def display(self):
        self.im.display(self.name)

