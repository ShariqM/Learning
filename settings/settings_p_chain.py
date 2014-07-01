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
MAZE    = 'gar##bage.txt'    # See files in maze_files/ dir
STEPS   = 1000              # Number of time steps to run
RUNS    = 500               # Number of runs

def init_strats():

    arr = []
    for r in range(30):
        for i in (120,124):
            im = ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True)
            arr.append(DyStrat(ENVIRON[0], im,
                                PigVIStrat(ENVIRON[0], im, PLUS=0, EXPLORER=False),
                                BossStrat(ENVIRON[0], im, -1), i))
    return arr
