cpdef autocorrelation(signal):

  if len(signal) == 0:
    return np.array([], dtype=np.int32)
  ft = np.fft.fft(signal)
  S = np.conj(ft)*ft

  # boilerplate
  warnings.filterwarnings(action="ignore", category=np.ComplexWarning)

  return np.round(np.fft.ifft(S)).astype(np.int32)
