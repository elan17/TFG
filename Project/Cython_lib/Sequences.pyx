# distutils: language = c++
cimport cython

from libcpp.set cimport set

from libc.stdlib cimport malloc, free

cimport numpy as np
import numpy as np

from cpython cimport array
import array

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef inline int legendre_symbol(int a, int p, set[int] * residues):
  cdef int m = a % p
  if residues.count(m):
    return 1
  else:
    return -1

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef int* legendre_sequence(int p):
  cdef int* r = <int *> malloc(p*sizeof(int))
  cdef set[int] * res = new set[int]()
  cdef int a, x
  for a in range(p // 2 + 1):
    res.insert((a*a) % p)
  for x in range(0, p):
    r[x] = legendre_symbol(x, p, res)
  del res
  return r


def py_legendre_sequence(int p):
  cdef array.array a = array.array('i', [])
  cdef int* r = legendre_sequence(p)
  l = []
  for x in range(p):
    l.append(r[x])
  free(r)
  return l
