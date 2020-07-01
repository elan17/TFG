import numpy as np
cimport numpy as cnp
cimport cython

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline double dot(double[:]slice1, double[:]slice2, Py_ssize_t l) nogil:
  cdef double r = 0
  for x in range(l):
    r += slice1[x] * slice2[x]
  return r

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def autocorrelation(cnp.ndarray[cnp.float64_t, ndim=1]vec):
    cdef Py_ssize_t x, l, off
    cdef double[:]n = vec
    cdef double[:]n1 = np.conj(vec)
    l = len(n)
    cdef double[:] returneo = np.empty_like(vec)
    cdef double[:]s1, s2, ns1, ns2
    for x in range(l):
        s1 = n[:x]
        s2 = n[x:]
        off = l-x
        ns1 = n1[off:]
        ns2 = n1[:off]
        returneo[x] = dot(s1, ns1, x) + dot(s2, ns2, off)
    return returneo
