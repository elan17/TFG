from setuptools import setup
from Cython.Build import cythonize
import numpy as np
import os
import cython_gsl

cyt = cythonize([   "bench_cython_unoptimized.pyx"
                    , "bench_cython_optimized.pyx"
                    , "bench_cython_gsl.pyx"]
                , annotate = True)

np_headers = np.get_include()
c_headers = [ np_headers
            , cython_gsl.get_cython_include_dir()]
library_dirs = [cython_gsl.get_library_dir()]
libs = cython_gsl.get_libraries()
for x in cyt:
    x.include_dirs += c_headers
    x.library_dirs += library_dirs
    x.libraries = libs
    x.cython_directives = {}
    x.cython_directives["infer_types"] = True


print(cyt[0].include_dirs)
setup(
    ext_modules = cyt
)
