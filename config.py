import sys
import math
from colors import *

# State nums (don't touch)
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint # Represents a new state we discovered
SS            = 0 # Start State

# Misc (don't touch)
NULL_ARG      = -999
NULL_UPDATE   = -9999
NUM_ACTIONS   = 4

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

from chinese import ChineseRProcess

# Run parameters
ENVIRON = None      # Ignore, initialized by the runner
MAZE    = 'maze.mz' # See files in maze_files/ dir
STEPS   = 30        # Number of time steps to run
RUNS    = 1         # Number of runs

# Output
DUMP_STDOUT = True # Dump the data to stdout
EXPORT_FILE = None # Export data to file
IMPORT_FILE = None # Import data and graph

# Graphics
GRAPHICS      = False # Visualization of agent
UPDATE_STEPMI = True  # Update Step, Missing Info
UPDATE_PIG    = False # Update Pig Table
UPDATE_VI     = False # Update Value Iteration Table (slow)

# Default parameters to models
ALPHA   = 0.99 # Discount parameter to a CRP
THETA   = 0.01 # Strength (or concentration) parameter to a CRP
D_ALPHA = 0.25 # Strength parameter to a Dirichlet model

# Strats to run [Choose a (Strategy, Internal Model) pair]
def init_strats():
    return [
  RandomStrat(ENVIRON,
              Dirichlet(ENVIRON), COLORS['red']),
  #RandomStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA), COLORS['red2']),

  UnembodiedStrat(ENVIRON,
              Dirichlet(ENVIRON),
              COLORS['black']),
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

  PigVIStrat(ENVIRON,
              Dirichlet(ENVIRON),
              COLORS['green'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, THETA, ALPHA),
              COLORS['red'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, 3.0, 0.0),
              COLORS['red'], PLUS=0, EXPLORER=False),

    # Experiments
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, 0.5, 0.5),
              COLORS['red'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, 0.50, 0.25),
              COLORS['red'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, 3.1, 0.0),
              COLORS['red'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
              ChineseRProcess(ENVIRON, 2.9, 0.0),
              COLORS['red'], PLUS=0, EXPLORER=False),

  PigVIStrat(ENVIRON,
              Dirichlet(ENVIRON),
              COLORS['blue'], PLUS=1, EXPLORER=False),
  #PigVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON),
              #COLORS['blue2'], PLUS=1, EXPLORER=False),

  #LTAStrat(ENVIRON,
              #ChineseRProcess(ENVIRON),
              #COLORS['yellow']),
  #LTAStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['yellow']),

  #LTAVIStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['purple3']),
           ]
