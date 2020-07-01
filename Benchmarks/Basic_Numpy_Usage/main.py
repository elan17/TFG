import numpy as np
import timeit
import bench_cpython as cpython
import bench_cython_unoptimized as cython_unoptimized
import bench_cython_optimized as cython_optimized
import bench_cython_gsl as cython_gsl
from copy import copy

n = 100000
seq = np.array([float(x%2) for x in range(n)], dtype=np.float64)

pretty_table = {
"cpython"            : "CPython:             ",
"cython_unoptimized" : "Cython unoptimized:  ",
"cython_optimized"   : "Cython optimized:    ",
"cython_gsl"         : "Cython GSL:          "
}

""" GATHER BENCHMARKS RESULTS """

call = "module.autocorrelation(seq)"

results = {}

print("RUNING TESTS. PLEASE WAIT")

def run_test(mod):
    return timeit.timeit(call, number=1, globals={ "module": globals().get(mod)
                                                 , "seq": globals().get("seq")})

def pretty_print(key, string):
    print(pretty_table[key] + string)

for x in pretty_table.keys():
    results[x] = run_test(x)
    pretty_print(x, str(results[x]))

""" COMPUTE THE PERCENTAGES  """

print("\nSPEEDUP RESULTS")

maxim = max(results.values())

results_percentage = {}
for x in results.keys():
    results_percentage[x] = results[x]/maxim

for x in results_percentage.keys():
    pretty_print(x, str(results_percentage[x]))
