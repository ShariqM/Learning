import sys
import math
from colors import *

# State nums (don't touch)
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint # Represents a new state we discovered
#SS            = 465 # Start State
SS            = 0 # Start State
MAX_REWARD    = 1.0
MASC          = 0.57721

# Misc (don't touch)
NULL_ARG      = -999
NULL_UPDATE   = -9999

# Maze Configuration
DETERMINISTIC = False # Noisy actions if false
WALL_CHAR     = '$'

# PIG Arguments
DISCOUNT_RATE = 0.95
VI_STEPS      = 10

# Parameters to Learning
UNK_PROB      = float("1e-5") # prob(K) for K not in your state space
BETA          = math.log(1.0 / UNK_PROB, 2) # Information gain of discovering a new state
import sys
# Knobs
FINIFY        = True # Break PSI into PSI' and K+1

# ------------ Common Arguments ------------ #
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from pigvistrat import *
from ltastrat import *
from ltavistrat import *
from cbstrat import *
from bossstrat import *
from bossSAstrat import *
from dystrat import *
from chainstrat import *
from randomstrat import *

from chinese import ChineseRProcess
from gamma import GammaProcess
from gampyp import GamPypProcess

# Run parameters
ENVIRON = []                # Ignore, initialized by the runner
#MAZE    = 'maze_s30_g.txt' # See files in maze_files/ dir
#MAZE    = 'maze_s30.mz'    # See files in maze_files/ dir
MAZE    = 'maze.mz'         # See files in maze_files/ dir
#MAZE    = 'maze_3d.mz'     # See files in maze_files/ dir
STEPS   = 200               # Number of time steps to run
RUNS    = 4                 # Number of runs
SERIAL  = False


# Output
DUMP_STDOUT = True  # Dump the data to stdout
EXPORT_FILE = None  # Export data to file
IMPORT_FILE = None  # Import data and graph

# Graphics
GRAPHICS      = False # Visualization of agent
UPDATE_STEPMI = True  # Update Step, Missing Info
UPDATE_PIG    = False  # Update Pig Table
UPDATE_VI     = False # Update Value Iteration Table (slow)

# Default parameters to models
ALPHA   = 0.0  # Discount parameter to a CRP
THETA   = 0.25 # Strength (or concentration) parameter to a CRP
D_ALPHA = 0.20 # Strength parameter to a Dirichlet model

# Strats to run [Choose a (Strategy, Internal Model) pair]
import numpy
def init_strats():
    arr = [
  #RandomStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['red']),
#
  #UnembodiedStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['black']),
#
  #PigVIStrat(ENVIRON[0],
              #Dirichlet(ENVIRON[0], D_ALPHA),
              #COLORS['blue'], PLUS=0, EXPLORER=False),
#
    #ES = int(3.0/4 * STEPS)
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #PigVIStrat(ENVIRON[0], im, PLUS=0, EXPLORER=False),
                       #BossSAStrat(ENVIRON[0], im, -1), ES, True))
#
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #LTAStrat(ENVIRON[0], im),
                       #BossSAStrat(ENVIRON[0], im, -1), ES, True))


  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA),
              COLORS['green'], PLUS=0, EXPLORER=False),

  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['purple'], PLUS=0, EXPLORER=False),
##
  #CBStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['purple']),
##
  #PigVIStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['grue2'], PLUS=1, EXPLORER=False),
  LTAStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['yellow2']),
        ]

    #for (t,ka) in [(0.001, math.log(2))]:
    #for (t,ka) in [(0.12, 0.13)]:
    for i in range(1):
        break
        for (t,ka) in [(math.log(2), 0.0), (0.38, 0.31), (0.001, 0.693), (0.001, math.log(2)), (0.001, 0.25), (0.120, 0.13)]:
            break
            max_k = 4 + 1.0 # Hacky... (Plus one for hypothetical new state)
            a = ka / max_k
            if a < 0.0 and not t + max_k * a > 0.0:
                continue
            if a >= 0.0 and not t > -a:
                continue
            if a > 1.0:
                continue
            if t == 0.0:
                continue

        arr.append(
      PigVIStrat(ENVIRON[0],
                 ChineseRProcess(ENVIRON[0], THETA, ALPHA),
                 COLORS['blue'], PLUS=0, EXPLORER=False))
        arr.append(
      PigVIStrat(ENVIRON[0],
                 ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
                 COLORS['green'], PLUS=0, EXPLORER=False))
        #arr.append(
      #PigVIStrat(ENVIRON[0],
                  #ChineseRProcess(ENVIRON[0], 0.001, 0.25, True),
                  #COLORS['green'], PLUS=0, EXPLORER=False))
        #arr.append(
      #PigVIStrat(ENVIRON[0],
                 #GamPypProcess(ENVIRON[0], 0.001, 0.25),
                 #COLORS['red'], PLUS=0, EXPLORER=False))
        #arr.append(
      #PigVIStrat(ENVIRON[0],
                  #ChineseRProcess(ENVIRON[0], 0.12, 0.13, True),
                  #COLORS['purple'], PLUS=0, EXPLORER=False))
        #arr.append(
      #PigVIStrat(ENVIRON[0],
                 #GammaProcess(ENVIRON[0], 0.25),
                 #COLORS['grue'], PLUS=0, EXPLORER=False))
        #arr.append(
      #PigVIStrat(ENVIRON[0],
                 #GammaProcess(ENVIRON[0], THETA),
                 #COLORS['green'], PLUS=0, EXPLORER=False))


    #ES = int(2.0/4 * STEPS)
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #PigVIStrat(ENVIRON[0], im, PLUS=0, EXPLORER=False),
                       #BossSAStrat(ENVIRON[0], im, -1), ES, True))
#
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #LTAStrat(ENVIRON[0], im),
                       #BossSAStrat(ENVIRON[0], im, -2), ES, True))
#
    return arr
