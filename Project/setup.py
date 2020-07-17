import os

paths = [
    ("Cython_lib/", "build_ext --inplace")
]

current_path = os.getcwd()

for x in paths:
    os.chdir(x[0])
    os.system("python setup.py {opts}".format(opts=x[1]))
    os.chdir(current_path)
