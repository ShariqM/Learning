"""
    Model is the super class of all internal and real models that are aware of
    all states.
"""

class Model(object):

    def get_states(self, a=-1, s=-1):
        return range(self.N)

    def has_state(self, s):
        return True

    def is_aware_of(self, a, s, ns):
        return True

    def get_prob(self, a, s, ns):
        raise Exception("get_prob not implemented")

    def display(self):
        print "a=Action, s=Starting State, ns=New state, p=Probability"
        print "For each (s,a) we display a list of (ns, p), the p of entering ns"
        i = 0
        for node in self.nodes:
            print "\tFrom Starting State=%d."% i
            for a in range(node.M):
                arr = []
                for ns in range(self.N):
                    if node.get_prob(a, ns) <= 0.0:
                        continue
                    arr.append((ns, round(node.get_prob(a, ns), 3)))
                print "\t\t(s=%d, a=%d) ->" % (i, a),  arr
            print ""
            i = i + 1

    def has_unknown_states(self):
        return False
