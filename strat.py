from ifunctions import *
import config

class Strat(object):

    def init(self, tm, im):
        self.tm = tm
        self.im = im
        self.explorer = False
        self.data = []
        for s in range(tm.N):
            self.data.append([])
            for a in range(tm.get_num_actions(s)):
                self.data[s].append(0)

        self.mi = {config.SS: self.get_init_mi(config.SS)}

    def update_tm(self, tm):
        self.tm = tm

    def get_information_gain(self):
        return self.im.get_information_gain()

    def get_reward(self):
        return self.im.total_reward

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def get_sname(self):
        return "%s" % (self.name)

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def debug(self, msg):
        if self.debugl:
            print msg

    def get_init_mi(self, s):
        return [missing_information_as(self.tm, self.im, a, s) for a in
                            range(self.tm.get_num_actions(s))]

    def new_data(self, a, s, ns):
        # Update cache
        self.data[s][a] += 1
        self.mi[s][a] = missing_information_as(self.tm, self.im, a, s)
        if ns not in self.mi.keys():
            self.mi[ns] = self.get_init_mi(ns)

        if self.graphics:
            self.graphics.update(a, s, ns, self.data[s][a], sum(self.mi[s]))

    def display(self):
        self.im.display(self.name)
