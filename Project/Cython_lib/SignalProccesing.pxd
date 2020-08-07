import numpy as np
cimport numpy as np

cdef int c_max_hamming_autocorrelation(int* sequence, int length_seq)

cdef int * composite_with_autocorrelation(int* autocorrelation, int l_signal, int* shifts, int l_shifts)

cdef bint c_good_composite_autocorrelation( int* autocorrelation
                                          , int l_signal
                                          , int* shifts
                                          , int l_shifts
                                          , int threshold)

cpdef composition(np.ndarray[int, ndim=1] signal, np.ndarray[int, ndim=1]shifts)

cpdef autocorrelation(signal)
