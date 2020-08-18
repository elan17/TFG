import warnings

cimport cython
import numpy as np
cimport numpy as np

from libc.stdlib cimport malloc, free

cdef extern from "math.h":
  cdef int abs(int x)

np.import_array()

cpdef correlation(s1, s2):
  return s1 * s2

cpdef autocorrelation(signal):
  """
    Computes the autocorrelation of a signal through Wiener–Khinchin's algorithm

    signal -- signal to use

    returns : The correlation for each shift (np.ndarray[np.complex, ndim=1])
  """
  if len(signal) == 0:
    return np.array([], dtype=np.int32)
  ft = np.fft.fft(signal)
  S = np.conj(ft)*ft
  warnings.filterwarnings(action="ignore", category=np.ComplexWarning)
  return np.round(np.fft.ifft(S)).astype(np.int32)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef composition(np.ndarray[int, ndim=1] signal, np.ndarray[int, ndim=1]shifts):
  """
    Computes the composite signal from a base signal and a set of shifts

    signal -- base signal
    shifts -- set of shifts to apply to the base signal

    returns : the composite signal (np.ndarray[array_t, ndim=1])
  """
  cdef int l_signal = len(signal)
  cdef int l_shifts = len(shifts)
  cdef int output_size = l_signal * l_shifts
  output = np.empty(output_size, dtype=signal.dtype)
  cdef int [:] output_view = output
  cdef int [:] signal_view = signal
  cdef int [:] shifts_view = shifts
  cdef int s, x
  for x in range(output_size):
    s = shifts_view[x%l_shifts]
    output_view[x] = signal_view[(x+s)%l_signal]
  return output

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef good_composite_autocorrelation(np.ndarray[int, ndim=1]autocorrelation, np.ndarray[int, ndim=1] shifts, int threshold):
    return c_good_composite_autocorrelation(<int*>autocorrelation.data, len(autocorrelation), <int*>shifts.data, len(shifts), threshold)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef bint c_good_composite_autocorrelation( int* autocorrelation
                                          , int l_signal
                                          , int* shifts
                                          , int l_shifts
                                          , int threshold):
  cdef int output_size = l_signal * l_shifts
  cdef int output
  cdef int x, y, affected_column, current_shift, final_shift, positive_difference
  cdef bint is_constant_column
  cdef int constant_offset = l_signal + 1
  for x in range(1, output_size):
    output = 0
    positive_difference = l_signal - (x%l_signal)
    for y in range(l_shifts):
      affected_column =  shifts[(y+x)%l_shifts]
      is_constant_column = affected_column == constant_offset
      current_shift  =  (positive_difference + shifts[y]) % l_signal
      final_shift = (not is_constant_column)*abs(current_shift-affected_column)\
                 + is_constant_column*l_signal
      output = output + autocorrelation[final_shift]
    if output > threshold:
      return False
  return True


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef composite_autocorrelation(np.ndarray[int, ndim=1]signal, np.ndarray[int, ndim=1] shifts):
  cdef np.ndarray[int, ndim=1] autoc = autocorrelation(signal)
  cdef int * v = composite_with_autocorrelation(<int*>autoc.data, len(signal), <int*>shifts.data, len(shifts))
  l = len(signal) * len(shifts)
  arr = np.empty(l, dtype=np.int32)
  for x in range(l):
    arr[x] = v[x]
  free(v)
  return arr

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef int * composite_with_autocorrelation(int* autocorrelation, int l_signal, int* shifts, int l_shifts):
    cdef int output_size = l_signal * l_shifts
    cdef int* output = <int *> malloc(output_size*sizeof(int))
    cdef int x, y, affected_column, current_shift, final_shift, positive_difference
    for x in range(output_size):
      output[x] = 0
      positive_difference = l_signal - (x%l_signal)
      for y in range(l_shifts):
        affected_column =  shifts[(y+x)%l_shifts]
        current_shift  =  (positive_difference + shifts[y]) % l_signal
        final_shift = abs(current_shift-affected_column) # TODO: Bypass GIL (abs seems bugged as it detects it as a Python function, although it generate pure C code)
        output[x] = output[x] + autocorrelation[final_shift]
    return output


cpdef max_hamming_autocorrelation(np.ndarray[int, ndim=1] sequence):
  return c_max_hamming_autocorrelation(<int*> sequence.data, len(sequence))

cdef int c_max_hamming_autocorrelation(int* sequence, int length_seq):
  cdef int max_auto = 0
  cdef int displacement, current_auto, x
  for displacement in range(1, length_seq-1):
    current_auto = 0
    for x in range(0, displacement):
      current_auto += (sequence[x] == sequence[x+displacement])
    for x in range(displacement, length_seq):
      current_auto += (sequence[x] == sequence[x-displacement])
    if current_auto > max_auto:
      max_auto = current_auto
  return max_auto
