def maximal_sequence(n):
    f.<alpha> = GF(2**n)
    g = f.primitive_element()
    r = vector([(g^i).trace () for i in range(f.order()-1)]).change_ring(ZZ)
    return vector([x*2 - 1 for x in r])
