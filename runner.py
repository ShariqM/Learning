from world import World
from stratrandom import StratRandom

ssteps = steps = 200

w = World(3, 2)
sr = StratRandom(w)

while steps > 0:
    x = sr.compute_mi()
    if steps % (ssteps / 10) == 0:
        print "Missing info: ", x
    sr.step()
    steps = steps - 1

w.display()
sr.display()
