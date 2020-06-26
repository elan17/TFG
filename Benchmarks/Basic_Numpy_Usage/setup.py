from setuptools import setup
from Cython.Build import cythonize
import numpy as np
import os

cyt = cythonize([ "bench_cython_unoptimized.pyx"
                        , "bench_cython_optimized.pyx"]
                        , annotate = True)

np_headers = np.get_include()
c_headers = [np_headers]
for x in cyt:
    x.include_dirs += c_headers


print(cyt[0].include_dirs)
setup(
    ext_modules = cyt
)
