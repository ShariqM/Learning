"""
    Hypothetical is a wrapper around an internal model to create a hypothetical
    model that takes the internal model and adds an observation a,s,ns. This is used
    to calculate Predicted Information Gain (PIG)
"""
import sys
import config

class Hypothetical:

    def __init__(self, im, a, s, ns):
        self.im = im
        self.a = a
        self.s = s
        self.ns = config.ETA if ns == config.PSI else ns

    def get_states(self, a, s):
        if self.ns == config.ETA:
            return self.im.get_states(a, s) + [self.ns]
        return self.im.get_states(a, s)

    def get_prob_new(self):
        p = self.get_prob(self.a, self.s, config.ETA) if self.ns == config.ETA else 0
        return p + self.get_prob(self.a, self.s, config.PSI)

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

    def is_hypothetical(self):
        return True
