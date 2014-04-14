import sys
import math

# State nums
PSI           = -1 # Represents the unknown state
ETA           = sys.maxint
SS            = 0 # Start State

# PIG Arguments
DISCOUNT_RATE = 0.95
VI_STEPS      = 10

# Parameters to Learning
UNK_PROB      = float("1e-5") # prob(K) for K not in your state space
BETA          = math.log(1.0 / UNK_PROB, 2) # Information gain of discovering a new state

# Misc
NULL_ARG      = -999
NULL_UPDATE   = -9999
NUM_ACTIONS   = 4

GRAPHICS      = False
