cimport cython_gsl as gsl
import numpy as np
cimport numpy as np
cimport cython

cdef (gsl.gsl_vector *) convert_to_gsl(np.ndarray[np.float_t, ndim=1] vec):
    bl = gsl.gsl_block_alloc(0)
    bl.data = <double *> vec.data
    bl.size = len(vec)
    n = gsl.gsl_vector_alloc(0)
    n.size = bl.size
    n.stride = 1
    n.data = bl.data
    n.block = bl
    n.owner = 0
    return n

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def autocorrelation(np.ndarray[np.float64_t, ndim=1] vec):
    n1_numpy = np.conj(vec)
    cdef (gsl.gsl_vector *) n  = convert_to_gsl(vec)
    cdef (gsl.gsl_vector *) n1 = convert_to_gsl(n1_numpy)
    cdef Py_ssize_t x, l, off
    l = len(vec)
    cdef gsl.gsl_vector_view s1, s2, ns1, ns2
    cdef double[:] returneo = np.empty_like(vec)
    cdef double d1, d2
    for x in range(l):
        off = l-x
        off_ind = off%l
        s1 = gsl.gsl_vector_subvector(n, 0, x)
        s2 = gsl.gsl_vector_subvector(n, x, off)
        ns1 = gsl.gsl_vector_subvector(n1, off_ind, x)
        ns2 = gsl.gsl_vector_subvector(n1, 0, off)
        gsl.gsl_blas_ddot(&s1.vector, &ns1.vector, &d1)
        gsl.gsl_blas_ddot(&s2.vector, &ns2.vector, &d2)
        returneo[x] = d1 + d2
    gsl.gsl_vector_free(n)
    gsl.gsl_vector_free(n1)
    return returneo
