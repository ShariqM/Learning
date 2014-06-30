"""
    (I)nformation Functions (The Key ones in the paper)
"""

import math
import config
from imodels.hypothetical import *
from functions import *

# Given a true model and an internal model with the same state space,
# compute the kl divergence
def kl_divergence(tm, im, a, s, debug=False):
    klsum = 0
    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue
        im_prob = im.get_prob(a, s, ns)
        im_prob = 1 if not im_prob else im_prob # See note [1]
        klsum += tm_prob * log2(tm_prob / im_prob)

    return klsum

def old_ukl_divergence(tm, im, a, s):
    klsum = 0
    def_prob = 1.0 / tm.N

    for ns in range(tm.N):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0: # can't do log 0
            continue

        im_prob = def_prob
        if im.has_state(s):
            if im.is_aware_of(a, s, ns):
                im_prob = im.get_prob(a, s, ns)
            else:
                psi_prob = im.get_prob(a, s, config.PSI)
                nunk_states = tm.N - len(im.get_known_states(a, s))
                im_prob = psi_prob / nunk_states

        klsum += tm_prob * log2(tm_prob / im_prob)

    return klsum

def ukl_divergence(tm, im, a, s):
    klsum = 0
    neighbors = tm.get_neighbors(s)
    def_prob = 1.0 / len(neighbors)

    for ns in neighbors:
        tm_prob = tm.get_prob(a, s, ns)
        im_prob = def_prob
        if im.has_state(s):
            if im.is_aware_of(a, s, ns):
                im_prob = im.get_prob(a, s, ns)
            else:
                psi_prob = im.get_prob(a, s, config.PSI)
                nunk_states = len(neighbors) - len(im.get_known_states(a, s))
                im_prob = psi_prob / nunk_states

        klsum += tm_prob * log2(tm_prob / im_prob)

    return klsum

def missing_information(tm, im):
    misum = 0
    for s in range(tm.N):
        for a in range(tm.get_num_actions(s)):
            misum += ukl_divergence(tm, im, a, s)
    return misum

def missing_information_as(tm, im, a, s):
    return ukl_divergence(tm, im, a, s)

def alt(val):
    #if val < 0.0:
        #return 0.0
    return val

def sm_divergence(tm, im, a, s, debug=False):
    #if not im.has_state(s):
        #return 1 / 0

    div = 0.0
    for ns in im.get_known_states(a, s):
        tm_prob = tm.get_prob(a, s, ns)
        if tm_prob <= 0.0:
            continue
        im_prob = im.get_prob(a, s, ns)
        div += alt(tm_prob * log2(tm_prob / im_prob))
        if debug:
            print '\t tm: %f, im %f div: %f' % (tm_prob, im_prob, div)

    if config.FINIFY:
        if tm.is_hypothetical() and im.has_unknown_states(): # If CRP model
            im_prob = im.get_prob(a, s, config.PSI)
            tm_prob = tm.get_prob(a, s, config.PSI)
            if tm.ns == config.ETA:
                # Compare PSI' with PSI/2 and ETA with PSI/2
                f = im.get_finify_by()
                tm_prob_new = tm.get_prob(a, s, config.ETA)
                div += alt(tm_prob * log2((f / (f-1)) * tm_prob / im_prob))
                div += alt(tm_prob_new * log2(f * tm_prob_new / im_prob))
                if debug:
                    print '\t F - tmn: %f tm: %f, im %f div: %f' % (tm_prob_new, tm_prob, im_prob, div)
            else:
                div += alt(tm_prob * log2(tm_prob / im_prob))
                if debug:
                    print '\t F - tm: %f, im %f div: %f' % (tm_prob, im_prob, div)
                #if s == 0:
                    #print 'a=', a, div
                #print "HYPO tm=%.2f im=%.2f s=%d a=%d div=%.2f" % \
                          #(tm_prob_new, im_prob, s, a, div)
    else:
        # Compare (PSI' + ETA) with PSI
        im_prob = im.get_prob(a, s, config.PSI)
        tm_prob = tm.get_prob(a, s, config.PSI)
        if tm.ns == config.ETA:
            tm_prob += tm.get_prob(a, s, config.ETA)
        div += alt(tm_prob * log2(tm_prob / im_prob))

    return div

# TODO Need to make this an argument to runner
def divergence(tm, im, a, s, debug=False):
    if True:
        return sm_divergence(tm, im, a, s, debug)
    else:
        return kl_divergence(tm, im, a, s, debug)

def information_gain(im, a, s, ns, new_state):
    if new_state:
        ns = config.ETA
    hm = Hypothetical(im, a, s, ns)
    #print 'Start new_state=', new_state
    x = sm_divergence(hm, im, a, s)
    return x

def predicted_information_gain(im, a, s, explorer):
    pig = 0

    if s == config.PSI:
        if not config.FINIFY:
            return config.BETA if explorer else 0

        # Maybe I should account for PSI being a known state
        im_prob = 1.0
        tm_prob = im.get_prob_first_obs()
        tm_prob_new = 1.0 - tm_prob

        pig =  alt(tm_prob * log2(2 * tm_prob / im_prob))
        pig += alt(tm_prob_new * log2(2 * tm_prob_new / im_prob))
        pig += config.BETA if explorer else 0

        return pig

    for ns in im.get_states(a, s):
        hm = Hypothetical(im, a, s, ns)
        pig += im.get_prob(a, s, ns) * divergence(hm, im, a, s, False)

        if explorer:
            pig += im.get_prob(a, s, ns) * config.BETA if ns == config.PSI else 0

    assert pig > 0, "Pig was %f for s=%d, a=%d" % (pig, s, a)
    return pig

# Notes
# [1] We need to express certain outcomes as having 0 probability in 123World.
# If we don't we get in a loop where we repeatedly choose a single action that
# would gain us huge information about the model if it were possible but it's
# not.
