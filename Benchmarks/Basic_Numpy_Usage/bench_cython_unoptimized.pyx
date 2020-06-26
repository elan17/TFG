import numpy as np

def autocorrelation(vec):
    n = vec
    n1 = np.conj(n)
    l = len(n)
    returneo = []
    for x in range(0, l):
        s1, s2 = (n[:x], n[x:])
        off = l-x
        ns1, ns2 = (n1[off:], n1[:off])
        returneo.append(s1 @ ns1 + s2 @ ns2)
    return returneo
