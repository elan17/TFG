cdef int * composite_with_autocorrelation( int* autocorrelation
                                         , int l_signal
                                         , int* shifts
                                         , int l_shifts):
    cdef int output_size = l_signal * l_shifts
    cdef int* output = <int *> malloc(output_size*sizeof(int))
    cdef int x, y, affected_column, current_shift, final_shift, positive_difference
    cdef int constant_offset = l_signal
    for x in range(output_size):
      output[x] = 0
      positive_difference = l_signal - (x%l_signal)
      for y in range(l_shifts):
        affected_column =  shifts[(y+x)%l_shifts]
        current_shift  =  (positive_difference + shifts[y]) % l_signal
        final_shift = abs(current_shift-affected_column)
        output[x] = output[x] + autocorrelation_with_constant[final_shift]
    return output
