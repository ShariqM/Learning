import math

# Given a true model and an internal model, compute the kl divergence
def kl_divergence(tm, im, a, s):
    klsum = 0
    for ns in range(tm.N):
        true_over_internal = tm.get_prob(a, s, ns) / im.get_prob(a, s, ns)
        if true_over_internal > 0:
            klsum += tm.get_prob(a, s, ns) * math.log(true_over_internal, 2)
    return klsum

def missing_information(tm, im):
    if tm.N != im.N or tm.M != im.M:
        raise Exception("Incomparable models")
    misum = 0
    for s in range(tm.N):
        for a in range(tm.M):
            misum += kl_divergence(tm, im, a, s)

    return misum
