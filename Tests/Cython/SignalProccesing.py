import sys

from hypothesis import given, assume, seed
import hypothesis.strategies as st
import hypothesis.extra.numpy as hnp

from math import gcd

from time import sleep

import numpy as np

sys.path.append("../../Project")

import Cython_lib.SignalProccesing as SP

def soft_array_compare(arr1, arr2, precision_margin=10**(-10)):
    """
    Let's us compare arrays without carying of floating point precision
    """
    dif = np.absolute(arr1 - arr2)
    comp = max(dif) <= precision_margin
    return comp

@given(st.data())
def test_composite_autocorrelation(data):
    small_int = st.integers(min_value=2, max_value=25)
    signal_length = data.draw(small_int)
    shifts_length = data.draw(small_int)
    assume(gcd(signal_length, shifts_length) == 1) # Check if they are coprimes
    signal = data.draw(hnp.arrays(np.int64, signal_length, elements=st.integers(min_value=-1, max_value=1)))
    shifts = data.draw(hnp.arrays(np.int32, shifts_length, elements=st.integers(min_value=0, max_value=max(signal_length-1, 0))))
    arr1 = SP.autocorrelation(SP.composition(signal, shifts))
    arr2 = SP.composite_autocorrelation(signal, shifts)
    assert soft_array_compare(arr1, arr2)

if __name__ == "__main__":
    test_composite_autocorrelation()
