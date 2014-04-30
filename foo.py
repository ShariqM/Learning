import math
import numpy

def prob(T, a, clusters):
    N = sum(clusters)

    def new_prod(K):
        p = 1.0
        for i in range(K):
            p *= T + i * a
        return p

    def exist_prod():
        p = 1.0
        for c in clusters:
            for i in range(1,c):
                p *= i - a
        return p

    def divisor():
        g = math.gamma
        return g(T + N + 0.0) / g(T)

    return new_prod(len(clusters)) * exist_prod() / divisor()

def compute(t, a, c):
    x = prob(t, a, c)
    print x
    return x

# {34: 12, 28: 159, 22: 180}
# {11: 48, 28: 20, 23: 5}
a = 0.0
t = 1.0
s = 0.0

MIN_T = -5.0
MAX_T = 5.0
STEP_T = 0.02

MIN_A = -5.0
MAX_A = 1.0
STEP_A = 0.02

import data2
#clusters = [[3,40,45], [48,20,5], [2, 43], [19, 14], [46, 25, 9], [45, 9]]
clusters = data2.arr
N = len(clusters)
maxs = [0.0] * N
max_ts = [-1] * N
max_as = [-1] * N

for t in numpy.arange(MIN_T, MAX_T, STEP_T):
    for a in numpy.arange(MIN_A, MAX_A, STEP_A):
        K = len(clusters)
        if a < 0.0 and not t + K * a > 0.0:
            continue
        if a >= 0.0 and not t > -a:
            continue
        for i in range(N):
            x = prob(t, a, clusters[i])
            if x > maxs[i]:
                maxs[i] = x
                max_ts[i] = t
                max_as[i] = a
        #print 't=%f | a=%f - ' % (t,a), x, y

avgt = 0.0
avga = 0.0
for i in range(N):
    avgt += max_ts[i]
    avga += max_as[i]
    print clusters[i], '%', max_ts[i], max_as[i]
avgt /= N
avga /= N
print 'avgt=', avgt
print 'avga=', avga
#
#a = 0.0
#t = 1.0
#s = 0.0
#print 'N=2'
#s = compute(s, t, a, [1,1])
#s += compute(s, t, a, [2])
#print 's=', s
#
#print '\nN=3'
#s = 0.0
#s += compute(s, t, a, [3])
#s += compute(s, t, a, [2,1])
#s += compute(s, t, a, [1,2])
#s += compute(s, t, a, [1,1,1])
#print 's=', s

#a = 0.25
#t = 0.5
#
#print 'N=2'
#print prob(t, a, [1,1])
#print prob(t, a, [2])
#
#print '\nN=3'
#print prob(t, a, [3])
#print prob(t, a, [2,1]) * 3
#print prob(t, a, [1,1,1])
