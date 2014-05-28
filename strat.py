from ifunctions import *
import config

class Strat(object):

    def init(self, tm, im):
        self.explorer = False
        self.data = []
        for s in range(tm.N):
            self.data.append([])
            for a in range(tm.M):
                self.data[s].append(0)

        self.init_mi = [missing_information_as(tm, im, a, config.SS) for a in
                            range(tm.M)]
        self.mi = {config.SS: list(self.init_mi)}

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

    def new_data(self, a, s, ns):
        # Update cache
        self.data[s][a] += 1
        self.mi[s][a] = missing_information_as(self.tm, self.im, a, s)
        if ns not in self.mi.keys():
            self.mi[ns] = list(self.init_mi)

        if self.graphics:
            self.graphics.update(a, s, ns, self.data[s][a], sum(self.mi[s]))

    def display(self):
        self.im.display(self.name)
