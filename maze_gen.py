from random import shuffle, randrange

# Transform
def t(i):
    return 2 + 3 * i

def make_maze(w = 6, h = 6):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    for x in vis:
        print x
    space = [["w . . . "] * w + ['w'] for _ in range(h)] + [[]]
    border = [["w w w w "] * w + ['w'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: border[max(y, yy)][x] = "w . . . "
            if yy == y: space[y][max(x, xx)]  = ". . . . "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    for (a, b, c, d) in zip(border, space, space, space):
        print(''.join(a + ['\n'] + b + ['\n'] + c + ['\n'] + d))

make_maze()
