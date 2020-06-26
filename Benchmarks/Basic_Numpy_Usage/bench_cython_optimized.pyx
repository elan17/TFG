import numpy as np
cimport numpy as cnp
cimport cython

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline int dot(int[:]slice1, int[:]slice2) nogil:
  cdef Py_ssize_t l = len(slice1)
  cdef int r = 0
  for x in range(l):
    r += slice1[x] + slice2[x]
  return r

@cython.boundscheck(False)
@cython.wraparound(False)
def autocorrelation(cnp.ndarray[cnp.int32_t, ndim=1]vec):
    cdef Py_ssize_t x, l
    cdef int[:]n = vec
    cdef int[:]n1 = np.conj(vec)
    l = len(n)
    returneo = np.empty_like(vec)
    cdef int[:] returneo_view = returneo
    cdef int[:]s1, s2, ns1, ns2
    cdef int d1, d2
    np_dot = np.dot
    np_add = np.add
    for x in range(l):
        s1 = n[:x]
        s2 = n[x:]
        off = l-x
        ns1 = n1[off:]
        ns2 = n1[:off]
        d1 = dot(s1, ns1)
        d2 = dot(s2, ns2)
        returneo_view[x] = d1 + d2
    return returneo
