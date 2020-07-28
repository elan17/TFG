def maximal_sequence(n):
    F.<alpha> = GF(2**n)
    g = F.primitive_element()
    return vector([(g^i).trace() for i in range(2**n-1)])
