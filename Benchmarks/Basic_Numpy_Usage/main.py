import numpy as np
import timeit
import bench_cpython
import bench_cython_unoptimized
import bench_cython_optimized

n = 100000
seq = np.array([x%17 for x in range(n)], dtype="int32")

call = "module.autocorrelation(seq)"


print("CPython:             " + \
            str(timeit.timeit(call, number=1, globals={ "module": globals().get("bench_cpython")
                                                      , "seq": globals().get("seq")})))

print("Cython unoptimized:  " + \
            str(timeit.timeit(call, number=1, globals={ "module": globals().get("bench_cython_unoptimized")
                                                      , "seq": globals().get("seq")})))

print("Cython optimized:    " + \
            str(timeit.timeit(call, number=1, globals={ "module": globals().get("bench_cython_optimized")
                                                      , "seq": globals().get("seq")})))
