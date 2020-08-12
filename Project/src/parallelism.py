from mpi4py import MPI
from time import sleep
from random import random

import numpy as np

import Cython_lib.SignalProccesing as SP
import Cython_lib.branch_and_bound as bb

import sys

from storage import store_sequences

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
num_proccess = comm.Get_size()

def master(polling_delay, max_counter):
    counter = 0
    requests = []
    counter_deallocation = num_proccess - 1
    for x in range(1, num_proccess):
        requests.append(comm.issend(counter, dest=x, tag=11))
        counter += 1
    while counter_deallocation > 0:
        sleep(polling_delay)
        i, b, msg = MPI.Request.testany(requests)
        if b and i >= 0:
            if not counter < max_counter:
                comm.isend(-1, dest=i+1, tag=11)
                counter_deallocation -= 1
            else:
                requests[i] = comm.issend(counter, dest=i+1, tag=11)
                counter += 1

def slave( base_sequence, sequence_length, task_size
         , hamming_upper_limit, correlation_upper_limit):
    exit_var = False
    while not exit_var:
        data = comm.recv(source=0, tag=11)
        if data != -1:
            seq = int_to_shift_sequence(data, sequence_length, len(base_sequence), task_size)
            print(seq)
            r = bb.py_get_list_of_good_shifts( base_sequence, hamming_upper_limit
                                             , correlation_upper_limit, seq, task_size)
            store_sequences(r, rank)
        else:
            exit_var = True

def int_to_shift_sequence(integer, sequence_length, max_value, task_size):
    arr = np.zeros(sequence_length, dtype=np.int32)
    it = sequence_length - task_size
    for x in range(1, it):
        arr[x] = int(integer / (max_value ** (x-1))) % max_value
    return arr


polling_delay = float(sys.argv[1])
seq = np.array([1 if x != "0" else -1 for x in sys.argv[2]], dtype=np.int32)
shift_length = int(sys.argv[3])
task_size = int(sys.argv[4])
hamming = int(sys.argv[5])
correlation_upper_limit = int(sys.argv[6])

if rank == 0:
    master(polling_delay, len(seq)**(shift_length-task_size-1))
else:
    slave(seq, shift_length, task_size, hamming, correlation_upper_limit)
