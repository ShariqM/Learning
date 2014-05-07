"""
    Generates NxN mazes
    TODO: Add transporters
"""

from random import shuffle, randrange
import random
import pdb

import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-n", "--num", dest="n", default=2,
                    type=int, help="Create a NxN maze")
# Transform
def t(i):
    return 2 + 3 * i

def pretty_print(arr):
    for a in arr:
        for b in a:
            print b
        print ''

    #pos = [["w . 0 . "] * w + ['w'] for _ in range(h)] + [[]]
    #pos_2d = [zip(border, space, pos, space) for _ in range(h)] + [[[]]]
    #border_2d = [zip(border, space, lborder, space) for _ in range(l + 1)]
    #space_2d = [zip(border, space, space, space) for _ in range(h)] + [[[]]]

def get_space(w,h,l):
    space = []
    for _ in range(l):
        space.append([["w . . . "] * w + ['w'] for _ in range(h)] + [[]])
    return space

def get_border(w,h,l):
    border = []
    for _ in range(l):
        border.append([["w w w w "] * w + ['w'] for _ in range(h + 1)])
    return border

def get_side(w,h,l):
    side = []
    for _ in range(l):
        side.append([["w . w . "] * w + ['w'] for _ in range(h)] + [[]])
    return side

def make_maze(w = 10, h = 10, l = 10):

    space = get_space(w,h,l)
    border = get_border(w,h,l)
    side = get_side(w,h,l)

    vis = []
    for _ in range(l):
        vis.append([[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)])
    vis.append([[1] * (w + 1) for _ in range(h + 1)])

    num_tels = int(5/6.0 * w * h * l)

    def walk(x, y, z):
        vis[z][y][x] = 1

        d = [(x - 1, y, z), (x + 1, y, z),
             (x, y - 1, z), (x, y + 1, z),
             (x, y, z - 1), (x, y, z + 1)]
        shuffle(d)
        for (xx, yy, zz) in d:
            if vis[zz][yy][xx]: continue
            if xx != x: space[z][y][max(x, xx)]  = ". . . . "
            if yy != y: border[z][max(y, yy)][x] = "w . . . "
            if zz != z: side[max(z,zz)][x][y] = ". . . . "
            walk(xx, yy, zz)
    #pretty_print(vis)
    #walk(randrange(w), randrange(h), randrange(l))

    #border_2d = [zip(border, space, lborder, space) for _ in range(l + 1)]
    #space_2d = [zip(border, space, space, space) for _ in range(h)] + [[[]]]

    border_2d = []
    for z in range(l):
        border_2d.append(zip(border[z], border[z], border[z], border[z]))
    border_2d.append(zip(get_border(w,h,l)[0], get_border(w,h,l)[0],
                         get_border(w,h,l)[0], get_border(w,h,l)[0]))

    space_2d = []
    for z in range(l):
        space_2d.append(zip(border[z], space[z], space[z], space[z]))
    space_2d.append([])

    for d in zip(border_2d, space_2d, space_2d, space_2d):
        maze_string = ""
        for z in d:
            for y in z:
                for x in y:
                    print ''.join(x)

    #for i in range(l):
        #for a,b,c,d in zip(border[i], space[i], space[i], space[i])
    #number()

    #maze_string = ""
    #for (a, b, c, d) in zip(border, space, locs, space):
        #maze_string += (''.join(a + ['\n'] + b + ['\n'] + c + ['\n'] + d)) + '\n'
    #print maze_string

args = parser.parse_args()
make_maze(args.n, args.n, args.n)


#
    #def number():
        #g = random.randint(0, w * h)
        #i = 0
        #for s in range(len(space) - 1):
            ##if s == len(space.
            ##print locs[s]
            #locs.append([])
            #for l in range(len(space[s]) - 1):
                #arr = list(space[s][l])
                #arr[4] = str(i % 10) if i != g else 'g'
                #i = i + 1
                #locs[s].append(''.join(arr))
            #locs[s].append('w')
        #locs.append([])
