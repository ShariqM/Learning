import random
import math


# Compute N choose R
def choose(n, r):
    num = math.factorial(n)
    den = float(math.factorial(r) * math.factorial(n-r))
    return num / den

class WorldNode:

    # Find the probability we get an edge to the absorber node
    def prob_absorb(self, N, a):
        num = 1 - math.pow(0.75, a+1)
        den = float(choose(N - 1, a))
        return num / den

    # Given r > 0, r <= 1, find which target node we should make an edge to.
    # Return False if we find a target we already have
    def find_target(self, action, pabsorb, pnormal, r):
        for to in range(1, self.N):
            x = pabsorb + ((to) * pnormal)
            #print self.N - 1, " ", x, " ", r, " ", action, self.actions[action]
            print x, " ", r
            if x - r >= 0.0:
                if to in self.actions[action]: # dupe
                    return False
                print "Adding ", to
                self.actions[action].append(to)
                return True
        x = 1 / 0

    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.actions = []
        absorber = 0

        for action in range(M):
            self.actions.append([])
            pabsorb = self.prob_absorb(N, action)
            pnormal = (1 - pabsorb) / (self.N - 1)
            nodes_left = action + 1
            while nodes_left > 0:
                r = round(random.random(), 2)
                print "r=%f, pabsorb=%f, pnormal=%f" % (r, pabsorb, pnormal)
                if r < pabsorb:
                    if absorber in self.actions[action]: # dupe
                        continue # try again
                    print "Adding absorber", absorber
                    self.actions[action].append(absorber)
                else:
                    if not self.find_target(action, pabsorb, pnormal, r):
                        continue # try again
                nodes_left -= 1

    def get_prob(self, a, ns):
        return 1.0 / (a+1) if ns in self.actions[a] else 0

    def take_action(self, a):
        return random.sample(self.actions[a], 1)[0]
