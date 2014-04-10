"""
    (I)nformation Functions (The Key ones in the paper)
"""

import math
from hypothetical import *

UNK_PROB = float("1e-5")
UNK_PIG = math.log(1.0 / UNK_PROB, 2)
NS_IG = 5.0 # New state information gain

# klsum += tm.get_prob(a, s, ns) * abs(math.log(true_over_internal, 2))
# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]
        klsum += tm_prob * math.log(tm_prob / im_prob, 1.1)
        #klsum += max(tm_prob * math.log(tm_prob / im_prob, 1.1), 0.0)

    return klsum

#def sm_divergence(tm, im, a, s, debug=False):
    #div = 0
    #for ns in tm.get_states(a, s):
        #tm_prob = tm.get_prob(a, s, ns)
        #if tm_prob <= 0.0:
            #continue
        #im_prob = UNK_PROB
        #if im.has_state(s) and im.is_aware_of(a, s, ns):
            #im_prob = im.get_prob(a, s, ns) if im.is_aware_of(a, s, ns) else UNK_PROB
        #div += max(tm_prob * math.log(tm_prob / im_prob, 2), 0.0)
    #return div

# A more flexible divergence that can deal with unknown states
# is_aware_of is used to make the DirichletProcess probabilities sum to 1

def alt(val):
    if val < 0.0:
        return 0.0
    return val

def sm_divergence(tm, im, a, s, debug=False):
    if not im.has_state(s):
        return UNK_PIG

    div = 0
    for ns in im.get_known_states(a, s):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0:
            continue
        im_prob = im.get_prob(a, s, ns)
        div += alt(tm_prob * math.log(tm_prob / im_prob, 2))

    if tm.is_hypothetical() and im.has_unknown_states(): # If CRP model
        # compare psi' with psi/2 and k+1 with psi/2
        im_prob = im.get_prob(a, s, -1)
        tm_prob = tm.get_prob(a, s, -1)
        if tm.ns == sys.maxint:
            tm_prob_new = tm.get_prob(a, s, sys.maxint)
            div += alt(tm_prob * math.log(2 * tm_prob / im_prob))
            div += alt(tm_prob_new * math.log(2 * tm_prob_new / im_prob))
        else:
            div += alt(tm_prob * math.log(tm_prob / im_prob))

        #print "HYPO tm=%.2f im=%.2f s=%d a=%d div=%.2f" % \
                  #(tm_prob_new, im_prob, s, a, div)

    return div

# TODO Need to make this an argument to runner
def divergence(tm, im, a, s, debug=False):
    if True:
        return sm_divergence(tm, im, a, s, debug)
    else:
        return kl_divergence(tm, im, a, s, debug)

def missing_information(tm, im):
    misum = 0
    for s in range(tm.N):
        for a in range(tm.M):
            misum += divergence(tm, im, a, s)
    return misum

def predicted_information_gain(im, a, s, explorer):
    pig = 0

    if s == -1:
        return UNK_PIG if explorer else 0

    for ns in im.get_states(a, s):
        hm = Hypothetical(im, a, s, ns)
        pig += im.get_prob(a, s, ns) * divergence(hm, im, a, s, False)
        if ns == -1:
            print 's=%d, a=%d, p=%.2f' % (s, a, im.get_prob(a, s, ns))
        if explorer:
            pig += im.get_prob(a, s, ns) * UNK_PIG if ns == -1 else 0
        #pig += im.get_prob(a, s, ns) * UNK_PIG if ns == -1 else 0

    return pig

# Notes
# [1] We need to express certain outcomes as having 0 probability in 123World.
# If we don't we get in a loop where we repeatedly choose a single action that
# would gain us huge information about the model if it were possible but it's
# not.
