"""
    Maze represents the probability distribution of a specific test environment.
    Its scope is limited to returning new states given a current state and an
    action. It keeps no state about a user of the environment.
"""

import string
import sys
from functions import *

class Maze:

    def parse_maze(self, fname):
        desc = open(fname, 'r')

        l = desc.readline()
        w = len(l) / 2
        maze = []
        for i in range(w):
            maze.append([])
            for j in range(w):
                maze[i].append(' ')

        nstates = 0
        gwell = -1
        r = 0
        while l != '':
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

        print_maze(maze)
        return maze, nstates, gwell

    def __init__(self, fname):
        maze, nstates, gwell = self.parse_maze(fname)
        curr = 0
        for i in range(len(maze)):
            cols = (len(maze[i]) - 1) / 4
            for j in range(len(maze[i])):
                if maze[i][j] not in string.digits:
                    continue
                neighbors = []
                for x,y in ((0,1), (1,0), (0, -1), (-1, 0)):
                    #print '(i=%d, j=%d'% (i, j), maze[i][j], ' ', x, y
                    if maze[i-y][j+x] == 't': # 1 space away
                        neighbors.append(gwell)
                    elif maze[i-y*2][j+x*2] == 'w': # 2 spaces away
                        neighbors.append(curr)
                    elif maze[i-y*4][j+x*4] in string.digits:
                        neighbors.append(curr + 1 * x + cols * -y)
                    else:
                        print x,y
                        print maze[i-y*4][j+x*4]
                        raise Exception("Malformed Map, pos=%d" % curr)
                print "%spos=%d, neighbors=" % \
                        ('\t\t\t\t\t' if curr % 2 == 0 else ' ', curr), neighbors
                curr = curr + 1



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
