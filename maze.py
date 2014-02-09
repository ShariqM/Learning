"""
    Maze represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

import sys
from functions import *

class Maze:

    def build_maze(self, fname):
        desc = open(fname, 'r')

        l = desc.readline()
        w = len(l) / 2
        maze = []
        for i in range(w):
            maze.append([])
            for j in range(w):
                maze[i].append(' ')

        r = 0
        while l != '':
            c = 0
            for i in l:
                if i == ' ' or i == '\n':
                    continue
                print i
                print r,c
                maze[r][c] = i
                c = c + 1
            l = desc.readline()
            r = r + 1

        print_maze(maze)
        return maze

    def __init__(self, fname):
        maze = self.build_maze(fname)
        sys.exit(0)


    def take_action(self, s, a):
        node = self.nodes[s]
        return node.take_action(a)

    def get_prob(self, a, s, ns):
        return self.nodes[s].get_prob(a, ns)

    def display(self):
        i = 1
        print "*** 123World (Real) Model ***"
        for node in self.nodes:
            print "\t%d."% i
            ia = 0
            for a in node.actions:
                print "\t\t(%d)-->" % ia, [node.get_prob(ia, ns) for ns in
                range(self.N)]
                ia = ia + 1
            print "\n\n"
            i = i + 1

    def is_affected_by(self, a, s):
        return False
