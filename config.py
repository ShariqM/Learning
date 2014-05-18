import sys
import math
from colors import *

# State nums (don't touch)
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint # Represents a new state we discovered
SS            = 0 # Start State
MAX_REWARD    = 1.0

# Misc (don't touch)
NULL_ARG      = -999
NULL_UPDATE   = -9999

# Maze Configuration
DETERMINISTIC=False # Noisy actions if false

# PIG Arguments
DISCOUNT_RATE = 0.95
VI_STEPS      = 10

# Parameters to Learning
UNK_PROB      = float("1e-5") # prob(K) for K not in your state space
BETA          = math.log(1.0 / UNK_PROB, 2) # Information gain of discovering a new state

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

from chinese import ChineseRProcess

# Run parameters
ENVIRON = None           # Ignore, initialized by the runner
MAZE    = 'maze.mz'  # See files in maze_files/ dir
STEPS   = 800            # Number of time steps to run
RUNS    = 1              # Number of runs
SERIAL  = False


# Output
DUMP_STDOUT = True # Dump the data to stdout
EXPORT_FILE = None # Export data to file
IMPORT_FILE = None # Import data and graph

# Graphics
GRAPHICS      = False # Visualization of agent
UPDATE_STEPMI = True  # Update Step, Missing Info
UPDATE_PIG    = True  # Update Pig Table
UPDATE_VI     = False # Update Value Iteration Table (slow)

# Default parameters to models
ALPHA   = 0.0  # Discount parameter to a CRP
THETA   = 1.50 # Strength (or concentration) parameter to a CRP
D_ALPHA = 0.25 # Strength parameter to a Dirichlet model

# Strats to run [Choose a (Strategy, Internal Model) pair]
import numpy
def init_strats():
    arr = [
  #RandomStrat(ENVIRON,
              #Dirichlet(ENVIRON), COLORS['red']),
  #RandomStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA), COLORS['red2']),

  #UnembodiedStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['black']),
  #UnembodiedStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['grey']),

  # FIXME
  #PigGreedyStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['blue']),
  #PigGreedyStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['grue2']),

    #PigVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['red'], PLUS=0, EXPLORER=False),
  #CBStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['red']),
  #BossStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #5, COLORS['red']),

  #PigVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['red'], PLUS=0, EXPLORER=True),
  #PigVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['red'], PLUS=1, EXPLORER=False),
  #PigVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, 3.0, 0.0),
              #COLORS['red'], PLUS=0, EXPLORER=False),
  #LTAStrat(ENVIRON,
              #ChineseRProcess(ENVIRON),
              #COLORS['yellow']),
  #LTAVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON),
              #COLORS['purple3']),
        ]

        # Experiments
    MIN_T  = -5.0
    MAX_T  =  5.01
    STEP_T =  0.25

    MIN_A  = -1.0
    MAX_A  =  1.0 # Don't move above 1.0 o/w we have prob(prev state) = 0
    STEP_A =  0.25

    #for a in numpy.arange(0.01 , 1.0, 0.05):#numpy.arange(0.01, 1.0, 0.1):
        #arr.append(
            #PigVIStrat(ENVIRON,
                #Dirichlet(ENVIRON, a),
                #COLORS['green'], PLUS=0, EXPLORER=False))

    for t in numpy.arange(MIN_T, MAX_T, STEP_T):
        for a in list(numpy.arange(MIN_A, MAX_A, STEP_A)) + [0.99]:
            max_k = 4 + 1 # Hacky... (Plus one for hypothetical new state)
            if a < 0.0 and not t + max_k * a > 0.0:
                continue
            if a >= 0.0 and not t > -a:
                continue
            if a > 1.0:
                continue
            if t == 0.0:
                continue

            #for i in xrange(60,61,1):
            #for i in xrange(60,150,1):
                #im = ChineseRProcess(ENVIRON, t, a)
                #arr.append(DyStrat(ENVIRON, im,
                                   #PigVIStrat(ENVIRON, im, PLUS=0, EXPLORER=False),
                                   #BossSAStrat(ENVIRON, im, -1), i))
            arr.append(
                PigVIStrat(ENVIRON,
                    ChineseRProcess(ENVIRON, t, a),
                    COLORS['red'], PLUS=0, EXPLORER=False))

    # Later
  #LTAStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['yellow']),

           #]
    return arr
