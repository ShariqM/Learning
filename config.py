import sys
import math
from colors import *

# State nums
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint # Represents a new state we discovered
SS            = 0 # Start State

# Maze Configuration
DETERMINISTIC=False

# Misc
NULL_ARG      = -999
NULL_UPDATE   = -9999
NUM_ACTIONS   = 4

# PIG Arguments
DISCOUNT_RATE = 0.95
VI_STEPS      = 10

# Parameters to Learning
UNK_PROB      = float("1e-5") # prob(K) for K not in your state space
BETA          = math.log(1.0 / UNK_PROB, 2) # Information gain of discovering a new state

# Knobs (Modify these with arguments to mazerunner.py. Not here.)
FINIFY        = True


# ------------ Common Arguments ------------ #
from randomstrat import *
from unembodiedstrat import *
from piggreedystrat import *
from pigvistrat import *
from ltastrat import *
from ltavistrat import *

from chinese import ChineseRProcess

# Run parameters
ENVIRON = None # Ignore, initialized by the runner
MAZE    = 'maze.mz' # See files in maze_files/ dir
STEPS   = 20
RUNS    = 1

# Graphics
GRAPHICS      = False # Visualization of agent
UPDATE_STEPMI = True  # Update Step, Missing Info
UPDATE_PIG    = False # Update Pig Table
UPDATE_VI     = False # Update Value Iteration Table (slow)

# Default parameters to models
ALPHA=0.99   # Discount parameter to a CRP
THETA=0.01   # Strength (or concentration) parameter to a CRP
D_ALPHA=0.25 # Strength parameter to a Dirichlet model

# Strats [Choose a (Strategy, Internal Model) pair]
def init_strats():
    return [
  #RandomStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['red']),
  #RandomStrat(ENVIRON, DirichletProcess(ENVIRON), COLORS['red2']),
  #UnembodiedStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['black']),
  #UnembodiedStrat(ENVIRON, DirichletProcess(ENVIRON), COLORS['grey']),
  #PigGreedyStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['blue']),
  #PigGreedyStrat(ENVIRON, DirichletProcess(ENVIRON), COLORS['grue2']),
  #PigVIStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['green'], 0),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON, 0.01), COLORS['red'], 0),
  PigVIStrat(ENVIRON,
             Dirichlet(ENVIRON),
             COLORS['green'], PLUS=0, EXPLORER=False),
  PigVIStrat(ENVIRON,
             ChineseRProcess(ENVIRON, THETA, ALPHA),
             COLORS['red'], PLUS=0, EXPLORER=True),
  #PigVIStrat(ENVIRON,
             #DirichletProcess(ENVIRON, THETA, ALPHA),
             #COLORS['blue'], PLUS=0, EXPLORER=False),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON, ALPHA), COLORS['blue'],
    #0, False, True),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON, 4.0), COLORS['green'], 0),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON, 25.0), COLORS['yellow'], 0),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON, 100.0), COLORS['purple'], 0),
  #PigVIStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['blue'], 1),
  #PigVIStrat(ENVIRON, DirichletProcess(ENVIRON), COLORS['blue2'], 1),
  #LTAStrat(ENVIRON, DirichletProcess(ENVIRON), COLORS['yellow'])
  #LTAStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['yellow']),
  #LTAVIStrat(ENVIRON, Dirichlet(ENVIRON), COLORS['purple3'])
           ]
