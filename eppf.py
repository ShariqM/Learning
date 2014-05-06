import numpy.random as ran
import sys
import numpy
import random
import pdb
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt

def lh(t, a, clusters):
    N = sum(clusters)

    def new_prod(K):
        p = 1.0
        for i in range(K):
            p *= t + i * a
        return p

    def exist_prod():
        p = 1.0
        for c in clusters:
            for i in range(1,c):
                p *= i - a
        return p

    def divisor():
        p = 1.0
        for i in range(N):
            p *= t + i
        return p

    r = new_prod(len(clusters)) * exist_prod() / divisor()
    if r >= 1.0 or r <= 0.0:
        raise Exception('Invalid: ' + str(t)+' '+str(a)+' '+str(r))
    return r

def valid_prob(t, a, K):
    if a < 0.0 and not t + K * a > 0.0:
        return False
    if a >= 0.0 and not t > -a:
        return False
    if a > 1.0:
        return False
    return True

all_clusters = [
            [18, 44, 1], # t = 1.55 a= -0.5 r= 3.11288678331e-20
            #[37, 1], # t = 0.55 a= -0.25 r= 0.00265409298173
            #[8, 2, 2], # t = 6.61 a= -2.2 r= 2.64511878075e-05
            ]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

MIN_T  =  0.0
MAX_T  =  2.0
STEP_T =  0.05

MIN_A  = -1.0
MAX_A  =  1.00
STEP_A =  0.05

A = []
T = []
V = []
maxr = -1
for t in numpy.arange(MIN_T, MAX_T, STEP_T):
    for a in numpy.arange(MIN_A, MAX_A, STEP_A):
        for clusters in all_clusters:
            if not valid_prob(t, a, len(clusters)):
                continue
            r = lh(t, a, clusters)
            maxr = max(maxr, r)
            V.append(r)
i = 0
for t in numpy.arange(MIN_T, MAX_T, STEP_T):
    for a in numpy.arange(MIN_A, MAX_A, STEP_A):
        for clusters in all_clusters:
            if not valid_prob(t, a, len(clusters)):
                continue

            if V[i] == maxr:
                t_max = t
                a_max = a
                print 'MAX - t=', t, 'a=', a, 'r=', V[i]
            if V[i]/maxr > 0.2:
                #print 'BIG - t=', t, 'a=', a, 'r=', V[i]
                ax.scatter(t, a, V[i], c=V[i], vmin=0, vmax=maxr, s=10)
            elif random.random() < STEP_T/10.0:
                ax.scatter(t, a, V[i], c=V[i], vmin=0, vmax=maxr, s=10)
            i = i + 1
print 'max', maxr

ax.set_xlabel('Theta')
ax.set_ylabel('Alpha')
ax.set_zlabel('Prob')

plt.axis([MIN_T, MAX_T, MIN_A, MAX_A])
plt.show()

sys.exit(0)

i = 0
j = 0
Z = []
for t in numpy.arange(MIN_T, MAX_T, STEP_T):
    Z.append([])
    for a in numpy.arange(MIN_A, MAX_A, STEP_A):
        for clusters in all_clusters:
            if not valid_prob(t, a, len(clusters)):
                Z[j].append(0.0)
                continue
            Z[j].append(V[i])
            i = i + 1
    j = j + 1

pdb.set_trace()

x = numpy.arange(MIN_T, MAX_T, STEP_T)
print len(x), j
y = numpy.arange(MIN_A, MAX_A, STEP_A)
plt.axis([MIN_T, MAX_T, MIN_A, MAX_A])
plt.xlabel('Theta', fontdict={'fontsize':16})
plt.ylabel('Alpha', fontdict={'fontsize':16})
plt.plot(t_max, a_max, marker='x')
plt.contour(x, y, Z)
plt.colorbar()
plt.show()
