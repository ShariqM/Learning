"""
    Maze represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

import string
import sys
from functions import *
from mazenode import MazeNode
import config
import random
import math


class Maze():

    def __init__(self, fname):
        self.maze, self.N, uniforms, self.gwells = parse_maze(fname)
        self.M = 4 # fixme?
        self.nodes = []
        self.rnodes = []

        cols = (len(self.maze[0]) - 1) / 4
        curr = 0
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if type(self.maze[i][j]) != int:
                    continue
                neighbors = []

                # for each direction
                for x,y in ((0,-1), (1,0), (0, 1), (-1, 0)):

                    # Teleporters are 1 space away
                    if str(self.maze[i+y][j+x]) in string.letters:
                    #if self.maze[i+y][j+x] == 't':
                        neighbors.append(self.gwells[self.maze[i+y][j+x]])

                    # Walls are 2 spaces away
                    elif self.maze[i+y*2][j+x*2] == config.WALL_CHAR:
                        neighbors.append(curr)

                    # Neighbors are 4 spaces away
                    elif type(self.maze[i+y*4][j+x*4]) == int:
                        neighbors.append(curr + 1 * x + cols * y)
                    else:
                        print x,y
                        raise Exception("Malformed Maze, pos=%d" % curr)

                uniform = curr in uniforms
                self.nodes.append(MazeNode(self.M, neighbors, uniform))

                #y = int(math.floor(y/width_factor))
                #x = int(math.floor(x/width_factor))
                y = (i - 2) / 4
                x = (j - 2) / 4
                dist = math.sqrt(math.pow(15-y, 2) + math.pow(15-x, 2))
                self.rnodes.append(dist)

                curr = curr + 1

    def take_action(self, s, a):
        ns = self.nodes[s].take_action(a)
        return ns, self.rnodes[ns]

    def get_prob(self, a, s, ns, new_states=None):
        return self.nodes[s].get_prob(a, ns, new_states)

    def get_num_actions(self, s):
        return self.M

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
    uniforms = set()
    gwells = {}
    r = 0
    while l != '' and l != '\n':
        c = 0
        for i in l:
            if i == ' ' or i == '\n':
                continue
            if i in string.ascii_uppercase:
                gwells[i.lower()] = nstates
                i = str(nstates % 10)

            if i == '!':
                uniforms.add(nstates)
                i = str(nstates % 10)

            if i in string.digits:
                nstates = nstates + 1
                i = nstates - 1

            maze[r][c] = i
            c = c + 1

        l = desc.readline()
        r = r + 1

    return maze, nstates, uniforms, gwells

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
