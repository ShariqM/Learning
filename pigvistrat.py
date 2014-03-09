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

class PigVIStrat():

    def __init__(self, tm, im, proc, color, control=False, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(VI+)" if control else "PIG(VI)"
        if proc:
            self.name += " [proc]"
        self.color = color
        self.marker = marker
        self.plansteps = 10 # Number of steps to look in the future
        self.discount = 0.95 # Discount factor for gains in future
        self.control = control # VI+ if True (uses real model)
        self.nprocesses = multiprocessing.cpu_count()
        self.data = {}

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
        num_states = len(self.im.get_states())
        for ns in self.im.get_states():
            m = self.tm if self.control else self.im
            m_prob = 1.0/num_states if s == -1 else m.get_prob(a, s, ns)
            tsum += m_prob * self.best_value(all_futures[i-1], ns)

        return self.discount * tsum

    def update_state_division(self):
        # Multiprocess organization
        self.state_division = [] # describes which states go to which process
        all_states = self.im.get_states()
        nstates = len(all_states)
        remainder = nstates % self.nprocesses # remainder states
        states_pp = nstates / self.nprocesses # states per process
        end = 0
        j = 0
        for i in range(self.nprocesses):
            start = end
            end = end + states_pp + (1 if remainder > 0 else 0)
            remainder -= 1
            self.state_division.append(all_states[start:end])
        #print self.state_division

    def step(self, last_mi=1):
        if last_mi <= 0.0: # optimization: no more information to gain
            return

        global pigs
        pigs = []
        for a in range(self.im.M):
            pigs.append({})
            for s in self.im.get_states():
                pigs[a][s] = 0

        # Fill in the global pigs table
        def global_pigs(msg):
            if msg== "Failed":
                raise Exception("Process failed")
            sub_states, data = msg
            global pigs
            for s in sub_states:
                for a in range(self.im.M):
                    pigs[a][s] = data[a][s]

        self.update_state_division()
        p = Pool(self.nprocesses) # Pool of processes
        for i in range(self.nprocesses):
            sub_states = self.state_division[i]
            p.apply_async(subset_pigs, args=(self.im, sub_states),
                          callback=global_pigs)
        p.close()
        p.join()

        all_futures = [] # List of Q's from the paper
        for i in range(self.plansteps):
            all_futures.append([])
            for a in range(self.im.M):
                all_futures[i].append({})
                for s in self.im.get_states():
                    all_futures[i][a][s] = pigs[a][s] + \
                        self.future_gain(i, all_futures, a, s)

        max_fgain = -1
        best_a = -1
        future = all_futures[self.plansteps - 1]
        #print_pig(pigs)
        #print_future(future)
        #self.display()
        for a in range(self.im.M):
            if future[a][self.pos] > max_fgain:
                max_fgain = future[a][self.pos]
                best_a = a

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)

        #if not self.data.has_key((self.pos, best_a)):
            #self.data[(self.pos, best_a)] = 0
        #self.data[(self.pos, best_a)] = self.data[(self.pos, best_a)] + 1
        #print self.data
        #print "--- STEP --- (s=%d, a=%d, ns=%d)" % (self.pos, best_a, ns)
        self.pos = ns

    def display(self):
        self.im.display(self.name)

# Compute the pig for a subset of states, each process is assigned a subset
def subset_pigs(im, sub_states):
    data = []
    for a in range(im.M):
        data.append({})
        for s in sub_states:
            try:
                data[a][s] = predicted_information_gain(im, a, s)
            except Exception as e:
                print e
                #return "Failed" Why does this stop the exception...
    return (sub_states, data)
