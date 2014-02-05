from world import World
from stratrandom import StratRandom


ssteps = steps = 1000

w = World(15, 3)
sr = StratRandom(w)

initial_mi = sr.compute_mi()
step_x = [x for x in range(1, steps+1)]
data_y = []
while steps > 0:
    x = sr.compute_mi()
    if steps % (ssteps / 10) == 0:
        print "Missing info: ", x
    data_y.append(x)
    sr.step()
    steps = steps - 1


w.display()
sr.display()

try:
    import matplotlib.pyplot as plt
    plt.xlabel('Time (steps)')
    plt.ylabel('Missing Information (bits)')
    plt.title('1-2-3 Worlds')
    plt.axis([0, ssteps, 0, initial_mi * 1.1])
    plt.text(ssteps * 0.75, initial_mi * 0.9, '____', color='red')
    plt.text(ssteps * 0.82, initial_mi * 0.885, 'Random')
    plt.plot(step_x, data_y, '-r,')
    plt.show()
except:
    print "\n***WARNING***\nPlease install matplotlib to see a graph.\n***WARNING***"

