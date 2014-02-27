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

class Maze(Model):

    def __init__(self, fname):
        self.maze, self.N, gwell = parse_maze(fname)
        self.M = 4
        self.nodes = []

        curr = 0
        for i in range(len(self.maze)):
            cols = (len(self.maze[i]) - 1) / 4
            for j in range(len(self.maze[i])):
                if self.maze[i][j] not in string.digits:
                    continue
                neighbors = []

                # for each direction
                for x,y in ((0,1), (1,0), (0, -1), (-1, 0)):

                    # Teleporters are 1 space away
                    if self.maze[i-y][j+x] == 't':
                        neighbors.append(gwell)

                    # Walls are 2 spaces away
                    elif self.maze[i-y*2][j+x*2] == 'w':
                        neighbors.append(curr)

                    # Neighbors are 4 spaces away
                    elif self.maze[i-y*4][j+x*4] in string.digits:
                        neighbors.append(curr + 1 * x + cols * -y)
                    else:
                        raise Exception("Malformed Maze, pos=%d" % curr)

                self.nodes.append(MazeNode(neighbors))

                curr = curr + 1

    def take_action(self, s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    def get_neighbors(self, s):
        return self.nodes[s].get_neighbors()

    def display(self):
        print "*** Maze (Real) Model ***"
        super(Maze, self).display()

def init_maze(l):
    w = len(l) / 2
    maze = []
    for i in range(w):
        maze.append([])
        for j in range(w):
            maze[i].append(' ')
    return maze
def parse_maze(fname):
    desc = open(fname, 'r')

    l = desc.readline()
    maze = init_maze(l)

    nstates = 0
    gwell = -1
    r = 0
    while l != '' and l != '\n':
        c = 0
        for i in l:
            if i == ' ' or i == '\n':
                continue
            if i == 'g':
                gwell = nstates
                i = str(nstates % 10)
            if i in string.digits:
                nstates = nstates + 1

            maze[r][c] = i
            c = c + 1

        l = desc.readline()
        r = r + 1

    return maze, nstates, gwell

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
