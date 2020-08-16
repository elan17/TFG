cdef void get_list_of_good_shifts( int* autocorrelation
                                 , int  sequence_length
                                 , int* initial_shift # Shift sequence
                                 , int  shift_length
                                   # Index at which the recursion must start
                                 , int  fixed_shift_offset
                                 , int  hamming_upper_limit
                                 , int  correlation_upper_limit
                                   # linked list at which we must store
                                   # the results
                                 , list[int*]* sequence_list):
  cdef int x, hamming, new_shift_offset
  cdef bint result
  cdef int* stored_sequence
  if fixed_shift_offset < shift_length: # Recursive case
    for x in range(0, sequence_length):
      initial_shift[fixed_shift_offset] = x # We fix a new component on the shift
      new_shift_offset = fixed_shift_offset +1 # We move the pointer
      hamming = SP.c_max_hamming_autocorrelation(initial_shift, shift_length)
      if hamming < hamming_upper_limit: # If we don't prune, we keep on with
                                        # the recursion
        get_list_of_good_shifts( autocorrelation
                               , sequence_length
                               , initial_shift
                               , shift_length
                               , new_shift_offset
                               , hamming_upper_limit
                               , correlation_upper_limit
                               , sequence_list)
    # After recursion, we unitialized the new component
    initial_shift[fixed_shift_offset] = -fixed_shift_offset
  else: # Base case
    result = SP.c_good_composite_autocorrelation( autocorrelation
                                                , sequence_length
                                                , initial_shift
                                                , shift_length
                                                , correlation_upper_limit)
    if result: # If the sequence has good properties, we store it
      stored_sequence = <int*> malloc(shift_length*sizeof(int))
      for x in range(0, shift_length):
        stored_sequence[x] = initial_shift[x]
      sequence_list.push_front(stored_sequence)
