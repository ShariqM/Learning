from functions import *

class Strat(object):

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def get_name(self):
        return "%s (%s)" % (self.name, self.im.get_name())

    def debug(self, msg):
        if self.debugl:
            print msg

    def display(self):
        self.im.display(self.name)


