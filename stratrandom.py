import random
from uniform import Uniform
from functions import *

class StratRandom():

    def __init__(self, tm):
        self.tm = tm
        self.im = Uniform(tm)
        self.pos = 0

    def compute_mi(self):
        return missing_information(self.tm, self.im)

    def step(self):
        states = [x for x in range(self.tm.M)]
        action = random.sample(states, 1)[0]
        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)
        self.im.update(action, oldpos, self.pos)
        print "%d-->%d" % (oldpos, self.pos)

    def display(self):
        self.im.display()

