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

def kill_slaves():
    """
        Kill slave proccesses *gently* so MPI terminates
    """
    for x in range(1, num_proccess):
        comm.isend(-1, dest=x, tag=11)

def master( polling_delay # Time between polls
          , shift_length # Length of the shift sequence
          , task_size # Height of the sub trees
          , hamming # Max hamming autocorrelation
          , max_value # Length of the base sequence
          , verbose):
    requests = []
    arr = np.array([-x for x in range(shift_length)], dtype=np.int32)
    # Task iterator
    task_iter = task_iterator(arr, 1, task_size, max_value, hamming)
    try:
        for x in range(1, num_proccess): # Initialize first task
            requests.append(comm.issend(shift_to_int(next(task_iter), task_size), dest=x, tag=11))
    except StopIteration: # If there are not enough tasks
        kill_slaves()
        sleep(0.3)
        print("The number of tasks found where too low for the number of threads, "\
              "consider lowering the size of the task or assigning less cores")
        exit(0)


    for task in task_iter: # Iterate over all the tasks
        exit_var = False
        while not exit_var:
            i, b, msg = MPI.Request.testany(requests)
            if b and i >= 0: # If there is a finished task
                # assign new task
                requests[i] = comm.issend(shift_to_int(task, task_size), dest=i+1, tag=11)
                if verbose:
                    print(i+1, task)
                exit_var = True
    # Tell the slaves to exit
    kill_slaves()

def slave( base_sequence
         , sequence_length # Length of shifts sequences
         , task_size # Height of the sub trees
         , hamming_upper_limit
         , correlation_upper_limit
         , verbose):
    exit_var = False
    while not exit_var:
        # Recieve task
        data = comm.recv(source=0, tag=11)
        if data != -1: # If it's an actual task
            # Compute the task
            seq = int_to_shift_sequence(data, sequence_length, len(base_sequence)+1, task_size)
            r = bb.py_get_list_of_good_shifts( base_sequence, hamming_upper_limit
                                             , correlation_upper_limit, seq, task_size)
            # Store the results
            store_sequences(r, rank)
        else: # If there's no more tasks
            if verbose:
                print(rank, "EXITED")
            # Exit
            exit_var = True

def task_iterator(arr, current_offset, task_size, max_value, hamming):
    it = len(arr) - task_size
    ham_auto = SP.max_hamming_autocorrelation(arr) < hamming
    if ham_auto: # Prune
        if current_offset == it: # base case
            yield arr
        else: # recursive case
            for x in range(max_value+1): # For all possible shifts
                arr[current_offset] = x
                # Go one step deeper  
                yield from task_iterator(arr, current_offset+1, task_size, max_value, hamming)
            arr[current_offset] = -current_offset

def int_to_shift_sequence(integer, sequence_length, max_value, task_size):
    arr = np.zeros(sequence_length, dtype=np.int32)
    it = sequence_length - task_size
    for x in range(1, it):
        arr[x] = int(integer / (max_value ** (x-1))) % max_value
    return arr

def shift_to_int(seq, task_size):
    it = len(seq) - task_size
    r = 0
    for x in range(1, it):
        r += seq[x] ** (x-1)
    return r

if __name__ == "__main__":
    polling_delay = float(sys.argv[1])
    seq = np.array([1 if x != "0" else -1 for x in sys.argv[2]], dtype=np.int32)
    shift_length = int(sys.argv[3])
    task_size = int(sys.argv[4])
    hamming = int(sys.argv[5])
    correlation_upper_limit = int(sys.argv[6])
    verbose = sys.argv[7] == "true"

    if rank == 0:
        master(polling_delay, shift_length, task_size, hamming, len(seq), verbose)
    else:
        slave(seq, shift_length, task_size, hamming, correlation_upper_limit, verbose)
