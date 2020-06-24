from setuptools import setup
from Cython.Build import cythonize
import os

setup(
    ext_modules = cythonize("bench_cython.pyx")
)

os.system("gcc bench_c.c")
