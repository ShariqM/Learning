import math
import numpy.random as ran
import config
import random
from functions import *

def ukl_divergence(tm, im):
    klsum = 0
    M = len(tm)

    for ns in range(M):
        tm_prob = tm[ns]

        if im.is_aware_of(ns):
            im_prob = im.get_prob(ns)
        else:
            psi_prob = im.get_prob(config.PSI)
            nunk_states = M - len(im.get_known_states())
            im_prob = psi_prob / nunk_states

        klsum += tm_prob * log2(tm_prob / im_prob)

    return klsum

class CRP(object):

    def __init__(self, theta, alpha, kalpha=False):
        self.obs_num = 0
        self.data = {}
        self.theta = theta
        self.alpha = alpha
        self.kalpha = kalpha

        s = "KA" if kalpha else "A"
        self.name = "CRP (T=%.3f, %s=%.3f)" % (theta, s, alpha)

    def reset(self):
        self.data = {}
        self.obs_num = 0

    def get_name(self):
        return self.name

    def get_known_states(self):
        return self.data.keys()

    def update(self, ns):
        prev = self.data[ns] if self.data.has_key(ns) else 0
        self.data[ns] = prev + 1
        self.obs_num = self.obs_num + 1

    def is_aware_of(self, ns):
        return self.data.has_key(ns)

    def get_prob(self, ns):
        ntables = len(self.data)
        alpha = self.alpha / ntables if self.kalpha and ntables else self.alpha
        if not self.data.has_key(ns):
            assert ns == config.PSI
            return (self.theta + ntables * alpha) / \
                    (self.obs_num + self.theta)
        return (self.data[ns] - alpha) / (self.obs_num + self.theta)


def run(tm, models):
    runs = 400
    steps = 100 + 1

    mi = [[0 for i in range(steps)] for j in range(len(models))]

    r = 0
    while r < runs:
        s = 0
        while s < steps:
            ns = sample(tm)
            for j in range(len(models)):
                im = models[j]
                mi[j][s] += ukl_divergence(tm, im)
                im.update(ns)
            s = s + 1
        for im in models:
            im.reset()
        r = r + 1

    # Average
    for j in range(len(models)):
        for s in range(steps):
            mi[j][s] /= runs

    for j in range(len(models)):
        name = models[j].get_name()
        msg = 'tm.M=%d | %s ' % (len(tm), name)
        points = [0, 10, 100]
        for p in points:
            msg += "(Step=%d, MI=%.3f) " % (p, mi[j][p])
        print msg

models = [
          CRP(0.25, 0.0),
          CRP(1, 0.0),
          CRP(5, 0.0),
          CRP(100, 0.0),
         ]

for m in [4,10,50,100]:
    tm = ran.dirichlet([1.0/m] * m) # Uniform alpha's
    run(tm, models)
    print ''
