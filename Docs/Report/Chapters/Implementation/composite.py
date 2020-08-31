cdef bint c_good_composite_autocorrelation( int* autocorrelation
                                          , int l_signal
                                          , int* shifts
                                          , int l_shifts
                                          , int threshold):
  cdef int output_size = l_signal * l_shifts
  cdef int output
  cdef int x, y, affected_column, current_shift, final_shift, positive_difference
  for x in range(1, output_size):
    output = 0
    positive_difference = l_signal - (x%l_signal)
    for y in range(l_shifts):
      affected_column =  shifts[(y+x)%l_shifts]
      current_shift  =  (positive_difference + shifts[y]) % l_signal
      final_shift = abs(current_shift-affected_column)
      output = output + autocorrelation[final_shift]
    if output > threshold:
      return False
  return True
