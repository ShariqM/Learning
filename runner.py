from world import World
from uniform import Uniform
from stratrandom import StratRandom

steps = 90

w = World(3, 3)
w.display()
sr = StratRandom(w)
last_mi = 9999
while steps > 0:
    x = sr.compute_mi()
    print "Missing info: ", x
    #if x > last_mi:
        #print "Failure", 1 / 0
    #last_mi = x
    sr.step()
    steps = steps - 1

sr.display()
