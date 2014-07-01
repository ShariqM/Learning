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
SS      = 0
MAZE    = 'maze.mz'         # See files in maze_files/ dir
STEPS   = 3000              # Number of time steps to run
RUNS    = 200               # Number of runs

def init_strats():
    arr = [
  RandomStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['red']),

  UnembodiedStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['black']),

  PigVIStrat(ENVIRON[0],
              Dirichlet(ENVIRON[0], D_ALPHA),
              COLORS['blue'], PLUS=0, EXPLORER=False),

  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA),
              COLORS['green'], PLUS=0, EXPLORER=False),

  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['green2'], PLUS=0, EXPLORER=False),

  CBStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['purple']),

  PigVIStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['grue2'], PLUS=1, EXPLORER=False),

  LTAStrat(ENVIRON[0],
              ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              COLORS['yellow2']),
        ]

    return arr
