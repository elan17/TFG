import sys

from hypothesis import given, assume, seed, note
import hypothesis.strategies as st
import hypothesis.extra.numpy as hnp

from math import gcd

from time import sleep

import numpy as np

import unittest as ut

sys.path.append("../../Project")

import src.Cython_lib.SignalProccesing as SP

def soft_array_compare(arr1, arr2, precision_margin=10**(-10)):
    """
    Let's us compare arrays without caring of floating point precision
    """
    if len(arr1) != len(arr2):
        return False
    dif = np.absolute(arr1 - arr2)
    if not len(dif):
        return True
    comp = max(dif) <= precision_margin
    return comp

class TestAutocorrelation(ut.TestCase):

    def generator(self, data):
        small_int = st.integers(min_value=0, max_value=25)
        signal_length = data.draw(small_int)
        return data.draw(hnp.arrays(np.int32, signal_length, elements=st.integers(min_value=-1, max_value=1)))

    @given(st.data())
    def test_maximum_value(self, data):
        """
        Test that checks the maximum value of the autocorrelation
        """
        signal = self.generator(data)
        auto = SP.autocorrelation(signal)
        if not len(signal):
            return
        assert auto[0]-1 <  max(auto) < auto[0]+1
        assert max(auto) <= len(auto)+1

    @given(st.data())
    def test_minimum_value(self, data):
        """
        Test that checks the minimum value of the autocorrelation
        """
        signal = self.generator(data)
        auto = SP.autocorrelation(signal)
        if not len(signal):
            return
        assert min(auto) > -len(auto)-1

class TestCompositeAutocorrelation(ut.TestCase):

    """
    Test of composite_autocorrelation
    """

    def generator(self, data):
        # We define a limit in the case size so the tests are fast
        small_int = st.integers(min_value=0, max_value=25)
        signal_length = data.draw(small_int)
        shifts_length = data.draw(small_int)
        # We make an assumtion on how the lengths relate
        assume(gcd(signal_length, shifts_length) == 1) # Check if they are coprimes
        # We generate the signal and the sequence of shifts
        signal = data.draw(hnp.arrays(np.int32, signal_length, elements=st.integers(min_value=-1, max_value=1)))
        shifts = data.draw(hnp.arrays(np.int32, shifts_length, elements=st.integers(min_value=0, max_value=max(signal_length, 0))))
        return (signal, shifts)

    @given(st.data())
    def test_composite_autocorrelation(self, data):
        """
        The composite autocorrelation must be equivalent to the naive one
        """
        signal, shifts = self.generator(data)
        # We compute the autocorrelation by both methods
        arr1 = SP.autocorrelation(SP.composition(signal, shifts))
        arr2 = SP.composite_autocorrelation(signal, shifts)
        # We assert equality
        if not soft_array_compare(arr1, arr2):
            print(arr1)
            print(arr2)
            pass
        assert soft_array_compare(arr1, arr2)

    @given(st.data())
    def test_good_composite_autocorrelation(self, data):
        """
        good_composite_autocorrelation must compute the same autocorrelation to
        composite_autocorrelation
        """
        signal, shifts = self.generator(data)
        small_int = data.draw(st.integers(min_value=0, max_value=25))
        arr1 = SP.composite_autocorrelation(signal, shifts)
        truth = SP.good_composite_autocorrelation(SP.autocorrelation_with_constant(signal), shifts, small_int)
        if len(arr1) < 2:
            return
        assert truth == (max(arr1[1:]) <= small_int)

class TestHammingAutocorrelation(ut.TestCase):

    def generator(self, data):
        signal_length = data.draw(st.integers(min_value=0, max_value=25))
        return data.draw(hnp.arrays(np.int32, signal_length, elements=st.integers(min_value=0, max_value=10)))

    @given(st.data())
    def test_hamming_autocorrelation(self, data):
        """
        Bound limits of hamming autocorrelation
        """
        arr = self.generator(data)
        x, count = np.unique(arr, return_counts=True)
        count2 = [x if x != 1 else 0 for x in count]
        upper_limit = sum(count2)
        corr = SP.max_hamming_autocorrelation(arr)
        assert corr <= upper_limit
        assert corr >= 0

if __name__ == "__main__":
    ut.main()
