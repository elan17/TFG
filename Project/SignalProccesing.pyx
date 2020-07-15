cimport cython
import numpy as np
cimport numpy as np

np.import_array()

ctypedef fused array_t:
  np.int32_t
  np.int64_t
  np.float32_t
  np.float64_t
  np.complex

cpdef autocorrelation(signal):
  """
    Computes the autocorrelation of a signal through Wiener–Khinchin's algorithm

    signal -- signal to use

    returns : The correlation for each shift (np.ndarray[np.complex, ndim=1])
  """
  ft = np.fft.fft(signal)
  S = np.conj(ft)*ft
  return np.fft.ifft(S)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef composition(np.ndarray[array_t, ndim=1] signal, np.ndarray[np.int32_t, ndim=1]shifts):
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
  cdef array_t [:] output_view = output
  cdef array_t [:] signal_view = signal
  cdef int [:] shifts_view = shifts
  cdef int s, x
  for x in range(output_size):
    s = shifts_view[x%l_shifts]
    output_view[x] = signal_view[(x+s)%l_signal]
  return output

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef composite_autocorrelation(np.ndarray[array_t, ndim=1] signal, np.ndarray[np.int32_t, ndim=1]shifts):
  """
    Computes the autocorrelation of the composite signal from it's base signal
    and the set of shifts efficiently

    signal -- base signal
    shifts -- set of shifts

    returns : The correlation for each shift
  """
  cdef int l_signal = len(signal)
  cdef int l_shifts = len(shifts)
  cdef int output_size = l_signal * l_shifts
  output = np.zeros(output_size, dtype=np.complex)
  cdef np.complex [:] output_view = output
  cdef array_t [:] signal_view = signal
  cdef int [:] shifts_view = shifts
  cdef int x, y, affected_column, current_shift
  cdef np.complex [:] autoc = autocorrelation(signal)
  for x in range(output_size):
    for y in range(l_shifts):
      affected_column =  shifts_view[(y+x)%l_shifts]
      current_shift  =  (shifts_view[y] + x) % l_signal
      output_view[x] = output_view[x] + autoc[(current_shift-affected_column)%l_signal]
  return output