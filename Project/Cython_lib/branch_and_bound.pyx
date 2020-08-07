# distutils: language = c++
cimport cython
import numpy as np
cimport numpy as np

from libc.stdlib cimport malloc, free
from libcpp.list cimport list

import SignalProccesing as SP
cimport SignalProccesing as SP

def py_get_list_of_good_shifts( np.ndarray[int, ndim=1] sequence
                              , shift_length
                              , hamming_upper_limit
                              , correlation_upper_limit):
  cdef np.ndarray[int, ndim=1] autocorrelation = SP.autocorrelation(sequence)
  cdef list[int*]* l = new list[int*]()
  cdef int* autoc = <int*> autocorrelation.data
  cdef np.ndarray[int, ndim=1] shifts = np.empty(shift_length, dtype=np.int32)
  for y in range(len(shifts)):
    shifts[y] = -y
  get_list_of_good_shifts( autoc
                         , len(autocorrelation)
                         , <int*> shifts.data
                         , shift_length
                         , 1
                         , hamming_upper_limit
                         , correlation_upper_limit
                         , l)
  returneo = []
  cdef int* x
  for x in l[0]:
    lista = []
    for y in range(0, shift_length):
      lista.append(x[y])
    free(x)
    returneo.append(lista)
  del l
  return returneo


cdef void get_list_of_good_shifts( int* autocorrelation
                                 , int  sequence_length
                                 , int* initial_shift
                                 , int  shift_length
                                 , int  fixed_shift_offset
                                 , int  hamming_upper_limit
                                 , int  correlation_upper_limit
                                 , list[int*]* sequence_list):
  cdef int x, hamming, new_shift_offset
  cdef bint result
  cdef int* stored_sequence
  if fixed_shift_offset < shift_length:
    for x in range(0, sequence_length):
      initial_shift[fixed_shift_offset] = x
      new_shift_offset = fixed_shift_offset +1
      hamming = SP.c_max_hamming_autocorrelation(initial_shift, shift_length)
      if hamming < hamming_upper_limit:
        get_list_of_good_shifts( autocorrelation
                               , sequence_length
                               , initial_shift
                               , shift_length
                               , new_shift_offset
                               , hamming_upper_limit
                               , correlation_upper_limit
                               , sequence_list)
    initial_shift[fixed_shift_offset] = -fixed_shift_offset
  else:
    result = SP.c_good_composite_autocorrelation( autocorrelation
                                                , sequence_length
                                                , initial_shift
                                                , shift_length
                                                , correlation_upper_limit)
    if result:
      stored_sequence = <int*> malloc(shift_length*sizeof(int))
      for x in range(0, shift_length):
        stored_sequence[x] = initial_shift[x]
      sequence_list.push_front(stored_sequence)
