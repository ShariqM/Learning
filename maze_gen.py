from random import shuffle, randrange
import random

# Transform
def t(i):
    return 2 + 3 * i

def make_maze(w = 25, h = 15):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    space = [["w . . . "] * w + ['w'] for _ in range(h)] + [[]]
    border = [["w w w w "] * w + ['w'] for _ in range(h + 1)]
    locs = []

    num_tels = int(5/6.0 * w * h)

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: border[max(y, yy)][x] = "w . . . "
            if yy == y: space[y][max(x, xx)]  = ". . . . "
            walk(xx, yy)

    def number():
        g = random.randint(0, w * h)
        i = 0
        for s in range(len(space) - 1):
            #if s == len(space.
            #print locs[s]
            locs.append([])
            for l in range(len(space[s]) - 1):
                arr = list(space[s][l])
                arr[4] = str(i % 10) if i != g else 'g'
                i = i + 1
                locs[s].append(''.join(arr))
            locs[s].append('w')
        locs.append([])

    walk(randrange(w), randrange(h))
    number()

    maze_string = ""
    for (a, b, c, d) in zip(border, space, locs, space):
        maze_string += (''.join(a + ['\n'] + b + ['\n'] + c + ['\n'] + d)) + '\n'
    print maze_string

make_maze()
