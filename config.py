import sys
import math
from colors import *

# State nums (don't touch)
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint # Represents a new state we discovered
MAX_REWARD    = 1.0
MASC          = 0.57721

# Misc (don't touch)
NULL_ARG      = -999
NULL_UPDATE   = -9999

# Maze Configuration
DETERMINISTIC = False # Noisy actions if false
#RAN_UNIFORM   = False # Noisy actions if false
WALL_CHAR     = '$'
UNIFORM_CHAR  = '!' # Uniform distrbution

# PIG Arguments
DISCOUNT_RATE = 0.95
VI_STEPS      = 10

# Parameters to Learning
UNK_PROB      = float("1e-5") # prob(K) for K not in your state space
BETA          = math.log(1.0 / UNK_PROB, 2) # Information gain of discovering a new state

# Knobs
FINIFY        = True # Break PSI into PSI' and K+1
SNEW_KL        = -4.0
FNEW_KL        = -5.0

# ------------ Common Arguments ------------ #
from strats.randomstrat import *
from strats.unembodiedstrat import *
from strats.piggreedystrat import *
from strats.pigvistrat import *
from strats.ltastrat import *
from strats.ltavistrat import *
from strats.cbstrat import *
from strats.bossstrat import *
from strats.dystrat import *
from strats.chainstrat import *

from imodels.chinese import *
from imodels.dirichlet import *
#from imodels.gamma import *
#from imodels.gammapyp import *

# Run parameters
ENVIRON = []                # Ignore, initialized by the runner
SERIAL  = False

# Output
DUMP_STDOUT = False  # Dump the data to stdout
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

SETTINGS = 'settings_params'
settings = __import__('settings.%s' % SETTINGS, fromlist=['settings'])
MAZE     = settings.MAZE
STEPS    = settings.STEPS
RUNS     = settings.RUNS
SS       = settings.SS      # Start State

# Strats to run [Choose a (Strategy, Internal Model) pair]
import numpy
def init_strats():
    return settings.init_strats()
