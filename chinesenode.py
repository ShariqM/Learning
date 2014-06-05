"""
    A DirichletProcessNode encodes the internal probability distribution model for a
    single node. This is closely related to the Chinese Restaurant Process.
"""

import random
import math
import config

class ChineseRProcessNode:

    def __init__(self, im):
        self.data = []
        self.obs_num = []
        self.im = im
        self.M = im.M
        self.total_reward = [0 for i in range(self.M)]

        for action in range(self.M):
            self.data.append({}) # Number of times (s,a,ns) has been observed
            self.obs_num.append(0) # Num of times (s,a) has been observed

    def get_states(self, a):
        return self.data[a].keys()

    def is_aware_of(self, a, ns):
        return self.data[a].has_key(ns)

    def get_prob_first_obs(self):
        return (1.0 - self.im.alpha) / (1.0 + self.im.theta)

    def harm_approx(self, N):
        return math.log(N) + config.MASC + 1.0/(2 * N) - 1.0/(12 * math.pow(N, 2))

    def get_theta(self, a):
        ntables = len(self.data[a])
        theta = self.im.theta
        if self.im.mle and self.obs_num[a]:
            if self.obs_num[a] == 1:
                theta = config.THETA_OBS_TWO
            else:
                theta = ntables / self.harm_approx(self.obs_num[a])
        return theta

    # Generalization of CRP
    def get_prob(self, a, ns):
        ntables = len(self.data[a])
        alpha = self.im.alpha / ntables if self.im.kalpha and ntables else self.im.alpha
        theta = self.get_theta(a)

        if not self.data[a].has_key(ns):
            assert ns == config.PSI
            return (theta + ntables * alpha) / (self.obs_num[a] + theta)

        return (self.data[a][ns] - alpha) / (self.obs_num[a] + self.im.theta)

    def get_reward(self, a):
        if not self.obs_num[a]:
            return 0.0
        return self.total_reward[a] / self.obs_num[a] # Mean reward

    def update(self, a, ns, r=0.0):
        prev = self.data[a][ns] if self.data[a].has_key(ns) else 0
        self.data[a][ns] = prev + 1
        self.obs_num[a] = self.obs_num[a] + 1
        self.total_reward[a] += r

    # Used to undo hypothetical updates
    def undo_update(self, a, ns):
        if self.data[a][ns] == 1:
            self.data[a].pop(ns)
        else:
            self.data[a][ns] = self.data[a][ns] - 1
        self.obs_num[a] = self.obs_num[a] - 1

    def stats(self):
        for a in range(self.M):
            print 'a=%d ->' % a, self.data[a]
