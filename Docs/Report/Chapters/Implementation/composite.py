cdef bint c_good_composite_autocorrelation( int* autocorrelation_with_constant
                                          , int l_signal
                                          , int* shifts
                                          , int l_shifts
                                          , int threshold):
  cdef int output_size = l_signal * l_shifts
  cdef int output
  cdef int x, y, affected_column, current_shift, final_shift, positive_difference
  cdef int constant_offset = l_signal
  cdef bint is_constant_column, is_current_shift_constant, is_constant_correlation, is_constant_hit
  for x in range(1, output_size):
    output = 0
    positive_difference = l_signal - (x%l_signal)
    for y in range(l_shifts):
      affected_column =  shifts[(y+x)%l_shifts]
      is_constant_column = affected_column == constant_offset
      current_shift  =  (positive_difference + shifts[y]) % l_signal
      is_current_shift_constant = shifts[y] == constant_offset
      is_constant_correlation = is_constant_column*is_current_shift_constant
      is_constant_hit = is_constant_column or is_current_shift_constant
      final_shift = (not is_constant_hit)*abs(current_shift-affected_column)\
                 + is_constant_hit*l_signal
      output = output \
             + (not is_constant_correlation)*autocorrelation_with_constant[final_shift]\
             + is_constant_correlation*l_signal
    if output > threshold:
      return False
  return True
