from Tkinter import *
import pdb
import string
import time
from functions import *

# Parameters
SCALE=20
BACKGROUND_COLOR = formatColor(0,0,0)
WALL_COLOR       = formatColor(0,0,0)
TRANSPORT_COLOR  = formatColor(0,0,0.7)
WIDTH            = 3.2
OFFSET           = 10
DELAY            = 0.0

class MazeGraphics:

    def __init__(self, maze, nstates, gwell):
        self.maze = maze
        self.width = len(maze)
        self.ncols = (len(maze) - 1) / 4

        self.data = []
        for s in range(nstates):
            self.data.append([])
            for a in range(4):
                self.data[s].append(None)

        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        #root.minsize(300,300)
        root.geometry("500x500")

        self.canvas = Canvas(root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        for y in range(len(self.maze)):
            for x in range(len(maze[y])):
                if self.maze[y][x] == 'w':
                    self.handle_wall(x,y)
                elif self.maze[y][x] == 't':
                    self.handle_transporter(x,y)
                elif self.maze[y][x] == gwell:
                    self.handle_position(x,y)
                    self.handle_well(x,y)
                elif type(self.maze[y][x]) == int:
                    self.handle_position(x,y)

        l = SCALE / 2.0
        xx, yy = OFFSET + 2 * SCALE, OFFSET + 2 * SCALE
        self.agent = self.canvas.create_oval(xx - l, yy - l, xx + l, yy + l,
                        fill='green', width=2.0)
        self.canvas.update()
        time.sleep(DELAY)


    def handle_wall(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = SCALE / 2.0

        # vertical
        if x % 4 == 0:
            l0, l1 = l,l
            if y == 0 or self.maze[y-1][x] != 'w':
                l0 = 0
            if y == self.width-1 or self.maze[y+1][x] != 'w':
                l1 = 0
            self.canvas.create_line(xx, yy - l0, xx, yy + l1, width=WIDTH)

        # horizontal
        if y % 4 == 0:
            l0, l1 = l,l
            if x == 0 or self.maze[y][x-1] != 'w':
                l0 = 0
            if x == self.width-1 or self.maze[y][x+1] != 'w':
                l1 = 0
            self.canvas.create_line(xx - l0, yy, xx + l1, yy, width=WIDTH)

    def handle_transporter(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = SCALE - SCALE / 4.0
        off = SCALE - WIDTH - 2.0 # put transporters close to wall
        if x % 2 == 0: # horizontal
            off = -off if self.maze[y-1][x] == 'w' else off
            self.canvas.create_line(xx - l, yy + off, xx + l, yy + off,
                               fill=TRANSPORT_COLOR, width=WIDTH)
        else: # vertical
            off = -off if self.maze[y][x-1] == 'w' else off
            self.canvas.create_line(xx + off, yy - l, xx + off, yy + l,
                               fill=TRANSPORT_COLOR, width=WIDTH)

    def handle_position(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = SCALE / 4.0
        self.canvas.create_oval(xx - l, yy - l, xx + l, yy + l,
                                fill='black', width=2.0)

        s = self.maze[y][x]
        l = SCALE
        a = 0
        for dx,dy in ((0,-1), (1,0), (0,1), (-1, 0)):
            self.data[s][a] = self.canvas.create_text(xx + dx * l, yy + dy * l,
                                                width=0.1, fill='red', text='0')
            a = a + 1

    def handle_well(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        ll = SCALE / 4.0
        for l in (ll * 2.0, ll * 3.0, ll * 4.0):
            self.canvas.create_oval(xx - l, yy - l, xx + l, yy + l,
                                   outline='cyan', width=2.0)

    def update(self, a, s, ns, count):
        dxcol = (ns % self.ncols) - (s % self.ncols)
        dx = dxcol * 4
        dycol = ns / self.ncols - s / self.ncols
        dy = dycol * 4

        self.canvas.itemconfigure(self.data[s][a], text='%d' % count)
        self.canvas.move(self.agent, dx * SCALE, dy * SCALE)
        self.canvas.update()
        time.sleep(DELAY)
