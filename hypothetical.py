"""
    Hypothetical is a wrapper around an internal model to create a hypothetical
    model that takes the internal model and adds an observation a,s,ns. This is used
    to calculate Predicted Information Gain (PIG)
"""

class Hypothetical:

    def __init__(self, im, a, s, ns):
        self.im = im
        self.a = a
        self.s = s
        self.ns = ns

    #def get_states(self, a, s):
        #if self.im.has_unknown_states():
            #return self.im.get_states(a, s) + [-1]
        #return self.im.get_states(a, s)

    def __getattr__(self,attr):
        orig_attr = self.im.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                return orig_attr(*args, **kwargs)
            return hooked
        else:
            return orig_attr

    # Update with the hypothetical observation, calc get_prob, then undo update
    def get_prob(self, a, s, ns):
        self.im.update(self.a, self.s, self.ns)
        rv = self.im.get_prob(a, s, ns)
        self.im.undo_update(self.a, self.s, self.ns)
        return rv
