import timeit
import bench_cython as b
import bench_cpython as bs
import os

iterations = 2147483647

link_time  = timeit.timeit("os.system(\"./a.out 0\")", number=1, globals={"os": globals().get("os")})
total_time = timeit.timeit("os.system(\"./a.out {0}\")".format(iterations), number=1, globals={"os": globals().get("os")})
print("C:        " + str(total_time - link_time))
print("Cython:   " + str(timeit.timeit("b.fac({0})".format(iterations), number=1, globals={"b": globals().get("b")})))
print("CPython:  " + str(timeit.timeit("bs.fac({0})".format(iterations), number=1, globals={"bs": globals().get("bs")})))
