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

import numpy

# Run parameters
SS      = 0
MAZE    = 'maze_complex_s10b.mz'    # See files in maze_files/ dir
STEPS   = 3000                     # Number of time steps to run
RUNS    = 200                       # Number of runs


def init_strats():
    arr = []

    MIN_T  =  0.01
    MAX_T  =  1.52
    STEP_T =  0.05

    for t in numpy.arange(MIN_T, MAX_T, STEP_T):
        if t == 0.0:
            continue
        arr.append(
            PigVIStrat(ENVIRON[0],
                ChineseRProcess(ENVIRON[0], t, ALPHA),
                COLORS['red'], PLUS=0, EXPLORER=False))

    return arr
