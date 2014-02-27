"""
    Model is the super class of all internal and real models
"""

class Model(object):


    def get_prob(self, a, s, ns):
        raise Exception("get_prob not implemented")

    def display(self):
        print "a=Action, s=Starting State, ns=New state, p=Probability"
        print "For each (s,a) we display a list of (ns, p), the p of entering ns"
        i = 0
        for node in self.nodes:
            print "\tFrom Starting State=%d."% i
            ia = 0
            for a in node.actions:
                arr = []
                for ns in range(self.N):
                    if node.get_prob(ia, ns) <= 0.0:
                        continue
                    arr.append((ns, round(node.get_prob(ia, ns), 3)))
                print "\t\t(s=%d, a=%d) ->" % (i, ia),  arr
                ia = ia + 1
            print "\n"
            i = i + 1
