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

from config import *

# Run parameters
MAZE    = 'maze.mz'         # See files in maze_files/ dir
STEPS   = 300               # Number of time steps to run
RUNS    = 4                 # Number of runs

# Strats to run [Choose a (Strategy, Internal Model) pair]
import numpy
def init_strats():
    arr = [
  UnembodiedStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['black']),
  PigVIStrat(ENVIRON[0],
              Dirichlet(ENVIRON[0], D_ALPHA),
              COLORS['blue'], PLUS=0, EXPLORER=False),
          ]
    return arr
