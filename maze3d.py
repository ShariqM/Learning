"""
    Maze represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

import string
import sys
from functions import *
from mazenode import MazeNode
from model import Model
import config

class Maze3d(Model):

    def __init__(self, fname):
        self.maze, self.N, self.M, self.gwell = parse_maze(fname)

        self.nodes = []

        l = len(self.maze)
        n = (l - 1) / 4
        curr = 0
        for k in range(l):
            for j in range(l):
                for i in range(l):
                    if type(self.maze[k][j][i]) != int:
                        continue
                    neighbors = []

                    # for each direction (U,R,D,L,I,O)
                    d = ((0,-1,0), (1,0,0), (0,1,0), (-1,0,0),
                         (0,0,-1), (0,0,1))
                    for x,y,z in d:
                        # Teleporters are 1 space away
                        if self.maze[k+z][j+y][i+x] == 't':
                            neighbors.append(self.gwell)

                        # Walls are 2 spaces away
                        elif self.maze[k+z*2][j+y*2][i+x*2] == 'w':
                            neighbors.append(curr)

                        # Neighbors are 4 spaces away
                        elif type(self.maze[k+z*4][j+y*4][i+x*4]) == int:
                            neighbors.append(curr + (1 * x) + (n * y) +
                                             (n * n * z))
                        else:
                            raise Exception("Malformed Maze, pos=%d" % curr)
                    print "Curr=%d, neighbors=" % curr, neighbors
                    self.nodes.append(MazeNode(self.M, neighbors))

                    curr = curr + 1

    def take_action(self, s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def get_prob(self, a, s, ns, new_states=None):
        return self.nodes[s].get_prob(a, ns, new_states)

    def get_neighbors(self, s):
        return self.nodes[s].get_neighbors()

    def display(self):
        print "*** Maze (Real) Model ***"
        super(Maze3d, self).display()

def init_maze(l):
    w = len(l) / 2
    maze = []
    for i in range(w):
        maze.append([])
        for j in range(w):
            maze[i].append([])
            for k in range(w):
                maze[i][j].append(' ')
    return maze
def parse_maze(fname):
    desc = open(fname, 'r')

    l = desc.readline()
    maze = init_maze(l)
    nactions = 6

    nstates = 0
    gwell = -1
    z = 0
    r = 0
    while l != '':
        if l == '\n':
            z += 1
            r = 0
            l = desc.readline()
            continue
        c = 0
        for i in l:
            if i == ' ' or i == '\n':
                continue
            if i == 'g':
                gwell = nstates
                i = str(nstates % 10)
            if i in string.digits:
                nstates = nstates + 1
                i = nstates - 1

            maze[z][r][c] = i
            c = c + 1

        l = desc.readline()
        r = r + 1

    if z == 0:
        maze = maze[0]
        nactions = 4

    return maze, nstates, nactions, gwell

"""
An example:
w = wall, t = teleporter, . = nothing, 0 and 6 are states

w . 0 t w
w . . . w
w . . . w
w . . . w
w . 6 . w
w . t . w
w w w w w

"""
