import random
from uniform import Uniform

class StratRandom():

    def __init__(self, tm):
        self.tm = tm
        self.im = Uniform(tm)
        self.pos = 0

    def step(self):
        states = [x for x in range(self.tm.M)]
        action = random.sample(states, 1)[0]
        oldpos = self.pos
        self.pos = self.tm.take_action(self.pos, action)
        print "%d-->%d" % (oldpos, self.pos)

