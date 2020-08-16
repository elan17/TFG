def composite_autocorrelation(signal, shifts):
  l_signal = len(signal)
  l_shifts = len(shifts)
  output_size = l_signal * l_shifts
  output = np.zeros(output_size, dtype=np.complex)
  autoc = compute_autocorrelation(signal)
  for x in range(output_size):
    for y in range(l_shifts):
      affected_column =  shifts[(y+x)%l_shifts]
      current_shift  =  (shifts[y] - x) % l_signal
      output[x] = output[x] + autoc[abs(current_shift - affected_column)]
  return vector(output)
