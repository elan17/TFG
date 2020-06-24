

def fac(n):
    y = 1
    for x in range(1, n-1):
        y = (y*x) % n
    return y
