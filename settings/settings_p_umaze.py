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
SS      = 465
MAZE    = 'maze_s30.txt'    # See files in maze_files/ dir
STEPS   = 3000              # Number of time steps to run
RUNS    = 200               # Number of runs

def init_strats():
    arr = [
  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA),
              COLORS['green'], PLUS=0, EXPLORER=False),

  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['purple'], PLUS=0, EXPLORER=False),
          ]

    return arr
