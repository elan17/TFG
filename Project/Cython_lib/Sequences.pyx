# distutils: language = c++
cimport cython

from libcpp.set cimport set

cimport numpy as np
import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef inline int legendre_symbol(int a, int p, set[int] residues):
  cdef int m = a % p
  if residues.count(m):
    return 1
  else:
    return -1

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef np.ndarray[np.int, ndim=1] legendre_sequence(int p):
  arr = np.empty(shape=p, dtype=np.int32)
  cdef int[:] r = arr
  cdef set[int] res
  cdef int a, x
  for a in range(p // 2 + 1):
    res.insert((a*a) % p)
  for x in range(0, p):
    r[x] = legendre_symbol(x, p, res)
  return arr
