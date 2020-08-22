import getopt

from sys import argv

from math import gcd, sqrt, ceil

from src.Cython_lib.Sequences import py_legendre_sequence

import os

help = "usage: python main.py [option...] \n\
Options and arguments: \n\
-n : number of threads to use(must be compatible with your MPI enviroment)\n\
     Defaults to the MPI configuration default\n\
-p : delay between polls in the master thread(higher values will make the \n\
     slaves to wait more until the next task, lower values will increase CPU \n\
     usage of master)\
-s : length of the base sequence(in this version must be a prime number to generate \n\
     Legendre sequences. Other values have undefined behaviour)\n\
-l : length of shift sequences(this option must be coprime with value of -s, other \n\
     values have undefined behaviour)\n\
-t : size of the task for each thread(this option must be lower than the value \n\
     provided by -l, other values have undefined behaviour)\n\
-h : maximum hamming autocorrelation allowed(this option must be a positive integer \n\
     other values have undefined behaviour) Defaults to -l\n\
-c : maximum autocorrelation we are interested in(this option must be a positive integer \n\
     other values have undefined behaviour) Defaults to the square root of (-l*-s)\n\
-v : verbose mode"


opts = ([], [])
try:
    opts = getopt.getopt(argv[1:], "n:p:s:l:t:h:c:v", ["help"])
except:
    pass
    # TODO
opts = dict(opts[0])

if "--help" in opts:
    print(help)
    exit(0)

def error(string):
    print(string)
    exit(-1)

format_values = []

if "-n" in opts:
    v = opts["-n"]
    try:
        int(v)
    except:
        error("Invalid value of option -n")
    if int(v) < 0:
        error("Invalid value of option -n")
    format_values.append("-n {0}".format(v))
else:
    format_values.append("")

if "-p" in opts:
    v = opts["-p"]
    try:
        float(v)
    except:
        error("Invalid value of option -p")
    if float(v) <0:
        error("Invalid value of option -p")
    format_values.append(v)
else:
    format_values.append("0.01")

if "-s" in opts:
    v = opts["-s"]
    try:
        int(v)
    except:
        error("Invalid value of option -s")
    if int(v) <0:
        error("Invalid value of option -s")
    seq = py_legendre_sequence(int(v))
    seq = ["1" if x == 1 else "0" for x in seq]
    format_values.append("".join(seq))
else:
    error("Required option -s not provided")

if "-l" in opts:
    v = opts["-l"]
    try:
        int(v)
    except:
        error("Invalid value of option -l")
    if int(v) <0:
        error("Invalid value of option -l")
    if gcd(int(v), int(opts["-s"])) != 1:
        error("-l and -s aren't coprimes")
    format_values.append(v)
else:
    error("Required option -l not provided")

if "-t" in opts:
    v = opts["-t"]
    try:
        int(v)
    except:
        error("Invalid value of option -t")
    if int(v) < 0:
        error("Invalid value of option -t")
    if int(v) > int(opts["-l"]):
        error("Invalid value of option -t")
    format_values.append(v)
else:
    error("Required option -t not provided")

if "-h" in opts:
    v = opts["-h"]
    try:
        int(v)
    except:
        error("Invalid value of option -h")
    if int(v) < 0:
        error("Invalid value of option -h")
    format_values.append(v)
else:
    format_values.append(opts["-l"])

if "-c" in opts:
    v = opts["-c"]
    try:
        int(v)
    except:
        error("Invalid value of option -c")
    if int(v) < 0:
        error("Invalid value of option -c")
    format_values.append(v)
else:
    format_values.append(ceil(sqrt(int(opts["-l"]) * int(opts["-s"]))))

if "-v" in opts:
    format_values.append("true")
else:
    format_values.append("0")

command = "mpirun {0} --oversubscribe --use-hwthread-cpus python src/parallelism.py {1} {2} {3} {4} {5} {6} {7}".format(*format_values)
os.system(command)
