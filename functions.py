import math

# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s):
    klsum = 0
    for ns in range(1, tm.N + 1):
        true_over_internal = tm.get_prob(ns, s, i) / im.get_prob(ns, s, i)
        klsum += tm.get_prob(ns, s, i) * math.log(true_over_internal, 2)

    return klsum

def missing_information(tm, im):
    if tm.N != im.N or tm.M != im.M:
        x = 1 / 0 # Validation failure
    misum = 0
    for s in range(1, tm.N + 1):
        for a in range(1, tm.M):
            misum += kl_divergence(tm, im, a, s)

    return misum
