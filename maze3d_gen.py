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
def s(i):
    return 1 + 4 * i
def t(i):
    return 2 + 4 * i
def it(i):
    return (i-2) / 4

def pp(maze):
    for z in maze:
        for y in z:
            print ' '.join(y)
        print ''

def init_maze(w,h,l):
    maze = []
    for i in range(s(l)):
        maze.append([])
        for j in range(s(h)):
            maze[i].append([])
            for k in range(s(w)):
                maze[i][j].append('w')

    g = randrange(w * h * l)
    n = 0
    for i in range(s(l)):
        if i % 4 == 0:
            continue
        for j in range(s(h)):
            if j % 4 == 0:
                continue
            for k in range(s(w)):
                if k % 4 == 0:
                    continue
                if (i-2) % 4 == 0 and (k-2) % 4 == 0 and (j-2) % 4 == 0:
                    if n == g:
                        maze[i][j][k] = 'g'
                    else
                        maze[i][j][k] = str(n % 10)
                    n += 1
                else:
                    maze[i][j][k] = '.'

    return maze

def make_maze(w = 10, h = 10, l = 10):

    maze = init_maze(w,h,l)

    vis = []
    for _ in range(l):
        vis.append([[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)])
    vis.append([[1] * (w + 1) for _ in range(h + 1)])

    def walk(x, y, z):
        vis[z][y][x] = 1
        #print x,y,z

        d = [(x - 1, y, z), (x + 1, y, z),
             (x, y - 1, z), (x, y + 1, z),
             (x, y, z - 1), (x, y, z + 1)]
        tx,ty,tz = t(x), t(y), t(z)
        shuffle(d)
        for (xx, yy, zz) in d:
            if vis[zz][yy][xx]: continue

            wxx = (t(xx)+tx) / 2
            wyy = (t(yy)+ty) / 2
            wzz = (t(zz)+tz) / 2

            #print (xx,yy,zz)

            if xx != x:
                for zzz in range(tz-1,tz+2):
                    for yyy in range(ty-1,ty+2):
                        maze[zzz][yyy][wxx] = '.'
            if yy != y:
                for xxx in range(tx-1,tx+2):
                    for zzz in range(tz-1,tz+2):
                        maze[zzz][wyy][xxx] = '.'
            if zz != z:
                for xxx in range(tx-1,tx+2):
                    for yyy in range(ty-1,ty+2):
                        maze[wzz][yyy][xxx] = '.'
            walk(xx, yy, zz)

    walk(randrange(w), randrange(h), randrange(l))

    pp(maze)

args = parser.parse_args()
make_maze(args.n, args.n, args.n)
