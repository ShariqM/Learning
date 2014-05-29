from Tkinter import *
import pdb
import string
import time
import config
from functions import *
import matplotlib.pyplot as plt

# Parameters
BACKGROUND_COLOR = formatColor(0,0,0)
WALL_COLOR       = formatColor(0,0,0)
TRANSPORT_COLOR  = formatColor(0,0,0.7)
SCALE            = 6.0
FONTSIZE         = int(SCALE * 1.5)
OFFSET           = 10
DELAY            = 0.0
WIDTH            = SCALE / 3.0
TRANS_DIST       = int(SCALE/6.0)

# Drawing
PAUSER = False
TABLES = False
COUNTERS = False

class MazeGraphics:

    def __init__(self, name, tm):
        self.maze = tm.maze
        self.width = len(tm.maze)
        self.ncols = (len(tm.maze) - 1) / 4
        self.nstates = int(math.pow(self.ncols, 2))
        self.pos = {}
        self.pos_color = {}
        self.cmap = plt.get_cmap('autumn')

        self.data = []
        for s in range(self.nstates):
            self.data.append([])
            for a in range(tm.M):
                self.data[s].append(None)

        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.wm_title(name)
        height = self.ncols * 25 * SCALE / 6 + 60
        width = self.ncols * 27 * SCALE / 6 + (600 if TABLES else 0)
        dim = "%dx%d" % (width, height)
        root.geometry(dim)

        self.canvas = Canvas(root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        if TABLES:
            self.pig = SimpleTable(root, "PIG", self.nstates + 2, tm.M + 1)
            tx = self.width * SCALE + OFFSET
            self.canvas.create_window(tx, OFFSET, anchor = NW, window = self.pig)

            self.vi = SimpleTable(root, "VI", self.nstates + 2, tm.M + 1)
            tx = tx + 260 + OFFSET
            self.canvas.create_window(tx, OFFSET, anchor = NW, window = self.vi)

        self.stats = StatsTable(root, "Stats", 2, 2)
        ty = self.width * SCALE + OFFSET
        self.canvas.create_window(OFFSET, ty, anchor = NW, window = self.stats)

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):

                if self.maze[y][x] == config.WALL_CHAR:
                    self.handle_wall(x,y)
                elif self.maze[y][x] in tm.gwells.values():
                    self.handle_position(x,y)
                    self.handle_well(x,y)
                elif type(self.maze[y][x]) == int:
                    self.handle_position(x,y)

        # Need transporters on top of pos
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == config.WALL_CHAR:
                    continue
                if str(self.maze[y][x]) in string.ascii_lowercase:
                    self.handle_transporter(x,y)

        l = SCALE
        xx, yy = OFFSET + 2 * SCALE, OFFSET + 2 * SCALE
        self.agent = self.canvas.create_oval(xx - l, yy - l, xx + l, yy + l,
                        fill='green', width=0.0)

        s = config.SS
        dxcol = (s % self.ncols)
        dx = dxcol * 4
        dycol = s / self.ncols
        dy = dycol * 4
        self.canvas.move(self.agent, dx * SCALE, dy * SCALE)

        self.canvas.update()
        time.sleep(DELAY)

        #self.graph_dist(tm)

    def graph_dist(self, tm):
        dcanvas = Canvas(root)
        dcanvas.grid(column=0, row=0, sticky=(N, W, E, S))

        dist = SimpleTable(root, "PIG", self.nstates + 2, 5)
        tx = self.width * SCALE + OFFSET
        self.canvas.create_window(tx, OFFSET, anchor = NW, window = self.pig)

    def handle_wall(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = SCALE / 2.0

        # vertical
        if x % 4 == 0:
            l0, l1 = l,l
            if y == 0 or self.maze[y-1][x] != config.WALL_CHAR:
                l0 = 0
            if y == self.width-1 or self.maze[y+1][x] != config.WALL_CHAR:
                l1 = 0
            self.canvas.create_line(xx, yy - l0, xx, yy + l1, width=WIDTH)

        # horizontal
        if y % 4 == 0:
            l0, l1 = l,l
            if x == 0 or self.maze[y][x-1] != config.WALL_CHAR:
                l0 = 0
            if x == self.width-1 or self.maze[y][x+1] != config.WALL_CHAR:
                l1 = 0
            self.canvas.create_line(xx - l0, yy, xx + l1, yy, width=WIDTH)

    def handle_transporter(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = SCALE - SCALE / 16.0
        width = WIDTH
        if x % 2 == 0: # horizontal
            off = -TRANS_DIST if self.maze[y-1][x] == config.WALL_CHAR else TRANS_DIST
            #print 'off', off
            self.canvas.create_line(xx - l, yy + off, xx + l, yy + off,
                               fill=TRANSPORT_COLOR, width=width)
        else: # vertical
            off = -TRANS_DIST if self.maze[y][x-1] == config.WALL_CHAR else TRANS_DIST
            #print 'off', off
            self.canvas.create_line(xx + off, yy - l, xx + off, yy + l,
                               fill=TRANSPORT_COLOR, width=width)

    def handle_position(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        l = 1.6 * SCALE

        xx += 0.5
        yy += 0.5

        s = self.maze[y][x]

        self.pos[s] = self.canvas.create_rectangle(xx - l, yy - l, xx + l, yy +
                l, fill="white", width=0)
        #self.pos[s] = self.canvas.create_rectangle(xx, yy, xx+1, yy+1, fill="blue")
        #self.pos[s] = self.canvas.create_text(xx, yy, fill='blue', text=str(s),
                            #font=("Purisa", FONTSIZE))
        self.pos_color[s] = 60
        #self.canvas.create_oval(xx - l, yy - l, xx + l, yy + l,
                                #fill='black', width=2.0)

        if COUNTERS:
            l = SCALE * 1.1
            a = 0
            for dx,dy in ((0,-1), (1,0), (0,1), (-1, 0)):
                self.data[s][a] = self.canvas.create_text(xx + dx * l, yy + dy * l,
                                font=("Purisa", FONTSIZE-1), fill='grey', text='0')
                a = a + 1

    def handle_well(self, x, y):
        xx,yy = x * SCALE + OFFSET, y * SCALE + OFFSET
        #ll = SCALE / 4.0
        #for l in (ll * 2.0, ll * 3.0, ll * 4.0):
        ll = SCALE / 4.0
        #for l in (ll * 2.0, ll * 3.0, ll * 4.0):
        for l in (ll, ll * 5.0):
            self.canvas.create_oval(xx - l - 1, yy - l - 1, xx + l, yy + l,
                                   outline='cyan', width=1.0)

    def step(self, step, mi, nstates):
        self.stats.set(1, 0, step)
        self.stats.set(1, 1, nstates)
        if PAUSER and step % 500 == 0:
            time.sleep(5)
        #self.stats.set(1, 1, "%.2f" % mi)
        #self.stats.set(1, 2, nstates)

    def update_val(self, for_pig, a, s, val):
        if s == -1:
            s = self.nstates
        if for_pig:
            self.pig.set(s+1,a+1, "%.2f" % val)
        else:
            self.vi.set(s+1,a+1, "%.2f" % val)

    def update_pig(self, a, s, pig):
        self.update_val(True, a, s, pig)

    def update_vi(self, a, s, vi):
        self.update_val(False, a, s, vi)

    def update(self, a, s, ns, count, mi_s):
        dxcol = (ns % self.ncols) - (s % self.ncols)
        dx = dxcol * 4
        dycol = ns / self.ncols - s / self.ncols
        dy = dycol * 4


        val = int(min(255, 1.0/mi_s * 255))
        #print mi_s, val, self.pos_color[ns]
        #self.canvas.itemconfig(self.pos[ns], fill=(1.0,0.0,0.4))
        #val = self.pos_color[ns]
        color = self.cmap(val)
        color = "#%.2lx%.2lx%.2lx" % (color[0] * 255, color[1] * 255, color[2] * 255)
        #self.canvas.itemconfig(self.pos[ns], fill="#3f0000")
        self.canvas.itemconfig(self.pos[ns], fill=color)
        self.pos_color[ns] = min(255, self.pos_color[ns] + 5)


        if COUNTERS:
            self.canvas.itemconfigure(self.data[s][a], text='%d' % count)
        self.canvas.move(self.agent, dx * SCALE, dy * SCALE)
        self.canvas.update()
        time.sleep(DELAY)

class SimpleTable(Frame):
    def __init__(self, parent, name, rows=10, columns=2):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        #print 'cols', columns

        label = Label(self, text=name, fg="green",
                      borderwidth=0, width=5, height=0)
        label.grid(row=0, sticky="nsew", padx=1, pady=1)

        titles = ["S", "U", "R", "D", "L"]
        for row in range(rows):
            row = row+1
            current_row = []
            for column in range(columns):
                if row == 1: # Titles
                    label = Label(self, text=titles[column], font=("Purisa",FONTSIZE),
                                  borderwidth=0, width=5, height=0)
                elif column == 0: # State
                    t = "psi" if row == rows else "%d" % (row-2)
                    label = Label(self, text=t, font=("Purisa",FONTSIZE),
                                  borderwidth=0, width=5, height=0)
                else:
                    label = Label(self, text="-1.0", font=("Purisa",8),
                                  fg='grey', borderwidth=0, width=FONTSIZE, height=0)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value, fg='red')
        widget.update()

class StatsTable(Frame):
    def __init__(self, parent, name, rows=10, columns=1):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="black")
        self._widgets = []

        label = Label(self, text=name, fg="green",
                      borderwidth=0, width=5, height=0)
        label.grid(row=0, sticky="nsew", padx=1, pady=1)

        titles = ["Step", "# States", "MI"]
        for row in range(rows):
            row = row + 1
            current_row = []
            for column in range(columns):
                if row == 1: # Titles
                    label = Label(self, text=titles[column], font=("Purisa",10),
                                  borderwidth=0, width=5, height=0)
                else:
                    label = Label(self, text="0.0", font=("Purisa",8),
                                  fg='grey', borderwidth=0, width=10, height=0)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value, fg='red')
        widget.update()
