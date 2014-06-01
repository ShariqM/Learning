
import matplotlib.pyplot as plt
import numpy

steps = 5
step_points = numpy.arange(1, 5, 1.0)


MIN_T  = -5.0
MAX_T  =  5.01
STEP_T =  0.5

MIN_A  = -5.0
MAX_A  =  5.0 # Don't move above 1.0 o/w we have prob(prev state) = 0
STEP_A =  0.5

import math
def p(a, b):
    print a,b
    return math.pow(a, b)

K = 4
def gamma(t, theta, alpha):
    print "t,theta,alpha", t, theta, alpha
    a = p(t - alpha, t)
    b = p(theta + t, t)
    return a / (b-a)


plt.xlabel('Time (steps)', fontdict={'fontsize':24})
plt.ylabel('Gamma)', fontdict={'fontsize':24})
plt.title("Gamma", fontsize=26)
plt.axis([0, steps, 0, 5])

for t in numpy.arange(MIN_T, MAX_T, STEP_T):
    for ka in list(numpy.arange(MIN_A, MAX_A, STEP_A)) + [0.99]:
        #t = 0.001
        #ka = math.log(2)

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


        Y = []
        for step in step_points:
            try:
                Y.append(gamma(step, t, ka))
            except:
                Y.append(30)

        if 1 or Y[steps-1] > 5 and Y[steps-1] < 5.9:
            plt.plot(step_points, Y, label="t=%f ka=%f" % (t,ka))



lg = plt.legend(fontsize=20)
lg.draw_frame(False)
plt.show()
