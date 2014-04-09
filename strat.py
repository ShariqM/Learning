from ifunctions import *

class Strat(object):

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def debug(self, msg):
        if self.debugl:
            print msg

    def new_data(self, a, s, ns):
        self.data[s][a] += 1
        if self.graphics:
            self.graphics.update(a, s, ns, self.data[s][a])

    def display(self):
        self.im.display(self.name)
