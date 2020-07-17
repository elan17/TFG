import sys

from hypothesis import given, assume, seed
import hypothesis.strategies as st
import hypothesis.extra.numpy as hnp

from time import sleep

import numpy as np

sys.path.append("../../Project")

import Cython_lib.SignalProccesing as SP

precision_margin = 10.0**(-200)
def soft_array_compare(arr1, arr2):
    """
    Let's us compare arrays without carying of floating point precision
    """
    dif = np.absolute(arr1 - arr2)
    comp = max(dif) <= precision_margin
    if not comp:
        print(arr1)
        print(arr2)
        print(dif)
        exit()
    return comp

@given(st.data())
@seed(102411555924360395765910700497704526526)
def test_composite_autocorrelation(data):
    small_int = st.integers(min_value=2, max_value=5)
    signal_length = data.draw(small_int)
    shifts_length = data.draw(small_int)
    assume(signal_length % shifts_length != 0)
    assume(shifts_length % signal_length != 0)
    signal = data.draw(hnp.arrays(np.int64, signal_length, elements=st.integers(min_value=-1, max_value=1)))
    shifts = data.draw(hnp.arrays(np.int32, shifts_length, elements=st.integers(min_value=0, max_value=max(signal_length-1, 0))))

    print(signal)
    print(shifts)

    arr1 = SP.autocorrelation(SP.composition(signal, shifts))
    arr2 = SP.composite_autocorrelation(signal, shifts)
    assert soft_array_compare(arr1, arr2)

if __name__ == "__main__":
    test_composite_autocorrelation()
