from world import World
from uniform import Uniform
from stratrandom import StratRandom

steps = 20

w = World(10, 3)
w.display()
sr = StratRandom(w)
while steps > 0:
    print "Missing info: ", sr.compute_mi()
    sr.step()
    steps = steps - 1
