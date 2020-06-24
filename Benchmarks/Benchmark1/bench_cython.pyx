
def fac(int n):
    cdef int x, y
    y = 1
    for x in range(1, n-1):
        y = (y*x) % n
    return y
