"""
    An embodied agent explores the world with limitation on a position. It
    picks an action that maximizes its PIG
"""

import random
from dirichlet import Dirichlet
from bayesworld import *
from functions import *
from strat import Strat

from multiprocessing import Pool
import multiprocessing
import datetime

class PigVIStrat(Strat):

    def __init__(self, tm, im, color, control=False, marker=None):
        self.tm = tm
        self.im = im
        self.pos = 0
        self.name = "PIG(VI+)" if control else "PIG(VI)"
        self.color = color
        self.marker = marker
        self.plansteps = 10 # Number of steps to look in the future
        self.discount = 0.95 # Discount factor for gains in future
        self.control = control # VI+ if True (uses real model)
        self.nprocesses = multiprocessing.cpu_count()
        self.data = {}
        self.pig_cache = [{} for a in range(self.tm.M)]

    def compute_mi(self):
        return missing_information(self.tm, self.im)


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
        print "Iter"
        start = datetime.datetime.now()

        global pigs
        for a in range(self.im.M):
            for s in self.im.get_states():
                if self.pig_cache[a].has_key(s):
                    continue
                self.pig_cache[a][s] = predicted_information_gain(self.im, a, s)
        print "\t cache - ", (datetime.datetime.now() - start).microseconds

        pigs = self.pig_cache
        global all_futures
        all_futures = [] # List of Q's from the paper
        self.update_state_division()

        # Fill in the futures table
        def fill_future(i):
            def fill_future_i(msg):
                print msg
                if msg== "Failed":
                    raise Exception("Process failed")
                sub_states, data = msg
                print msg
                global all_futures
                for s in sub_states:
                    for a in range(self.im.M):
                        all_futures[i][a][s] = data[a][s]
            return fill_future_i

        im_states = self.im.get_states()
        m = self.tm if self.control else self.im
        for i in range(self.plansteps):
            print '\n'
            p = Pool(self.nprocesses) # Pool of processes
            all_futures.append([])
            for a in range(self.im.M):
                all_futures[i].append({})

            for j in range(self.nprocesses):
                sub_states = self.state_division[j]
                print sub_states
                future = None if i == 0 else all_futures[i-1]
                p.apply_async(subset_pigs, args=(m, im_states, pigs, future),
                              callback=fill_future(i))
            #for a in range(self.im.M):
                #all_futures[i].append({})
                #for s in self.im.get_states():
                    #all_futures[i][a][s] = pigs[a][s] + \
                        #self.future_gain(i, all_futures, a, s)

            p.close()
            p.join()
            print all_futures

        print "\t future - ", (datetime.datetime.now() - start).microseconds

        max_fgain = -1
        best_a = -1
        future = all_futures[self.plansteps - 1]
        for a in range(self.im.M):
            if future[a][self.pos] > max_fgain:
                max_fgain = future[a][self.pos]
                best_a = a

        self.pig_cache[best_a].pop(self.pos) # ASSUMPTION

        ns = self.tm.take_action(self.pos, best_a)
        self.im.update(best_a, self.pos, ns)
        self.pos = ns

        print "\t end - ", (datetime.datetime.now() - start).microseconds

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def display(self):
        self.im.display(self.name)

def best_value(m, future, s):
    tmax = -1
    for a in range(m.M):
        tmax = max(tmax, future[a][s])
    return tmax

def future_gain(m, states, future, a, s):
    if not future:
        return 0

    tsum = 0
    num_states = len(states)
    for ns in states:
        m_prob = 1.0/num_states if s == -1 else m.get_prob(a, s, ns)
        tsum += m_prob * best_value(m, future, ns)

    return self.discount * tsum

# Compute the pig for a subset of states, each process is assigned a subset
def subset_pigs(m, state, pigs, future):
    data = []
    for a in range(m.M):
        data.append({})
        for s in sub_states:
            try:
                data[a][s] = pigs[a][s] + future_gain(m, states, future, a, s)
            except Exception as e:
                raise e
                #print e
                return "Failed" # Why does this stop the exception...
    return (sub_states, data)
