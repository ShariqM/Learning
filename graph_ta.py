import matplotlib.pyplot as plt
import tadata


#(0.500, 0.250, 236.796196607),

data = tadata.arr
Ts = set()
As = set()
values = {}
for (T, A, mi) in data:
    Ts.add(T)
    As.add(A)

    if not values.has_key(T):
        values[T] = {}
    values[T][A] = mi

Ts = list(Ts)
Ts.sort()
As = list(As)
As.sort()

Ts = Ts[7:13]
print 'Ts=', Ts
print 'As=', As
#print 'vals', values

V = []
i = 0
for t in Ts:
    V.append([])
    for a in As:
        if values.has_key(t) and values[t].has_key(a):
            V[i].append(values[t][a])
        else:
            V[i].append(0.0) #hmm
    i = i + 1
print 'V=', V
#plt.plot(Ts, As)
plt.contour(Ts, As, V)
plt.show()
