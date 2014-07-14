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

# Run parameters
SS      = 0
MAZE    = 'maze.mz'         # See files in maze_files/ dir
STEPS   = 300               # Number of time steps to run
RUNS    = 4                 # Number of runs

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
  PigVIStrat(ENVIRON[0],
              Dirichlet(ENVIRON[0], D_ALPHA),
              COLORS['blue'], PLUS=0, EXPLORER=False),
#
    #ES = int(3.0/4 * STEPS)
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #PigVIStrat(ENVIRON[0], im, PLUS=0, EXPLORER=False),
                       #BossStrat(ENVIRON[0], im, -1), ES, True))
#
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #LTAStrat(ENVIRON[0], im),
                       #BossStrat(ENVIRON[0], im, -1), ES, True))


  #PigVIStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA),
              #COLORS['green'], PLUS=0, EXPLORER=False),
#
  #PigVIStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['purple'], PLUS=0, EXPLORER=False),
##
  #CBStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['purple']),
##
  #PigVIStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['grue2'], PLUS=1, EXPLORER=False),
  #LTAStrat(ENVIRON[0],
              #ChineseRProcess(ENVIRON[0], THETA, ALPHA, False, True),
              #COLORS['yellow2']),
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
                       #BossStrat(ENVIRON[0], im, -1), ES, True))
#
    #im = ChineseRProcess(ENVIRON[0], THETA, ALPHA)
    #arr.append(DyStrat(ENVIRON[0], im,
                       #LTAStrat(ENVIRON[0], im),
                       #BossStrat(ENVIRON[0], im, -2), ES, True))
#
    return arr
