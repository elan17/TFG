from setuptools import setup
import numpy as np
from Cython.Build import cythonize

cyt = cythonize([ "SignalProccesing.pyx"
                , "Sequences.pyx"  
                ]
                , annotate = True)

c_headers    = [ np.get_include()
               ]
library_dirs = []
libs         = []
for x in cyt:
    x.include_dirs                     += c_headers
    x.library_dirs                     += library_dirs
    x.libraries                        =  libs
    x.cython_directives                =  {}
    x.cython_directives["infer_types"] =  True

setup(
    ext_modules = cyt,
    install_requires = [
        "cython",
        "numpy"
    ]
)
