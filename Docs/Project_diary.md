### 24/06/2020

##### Work done

* Created a benchmarks folder to support the use of Cython for the computations
* Learned the basics of Cython through the [online documentation] (https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html)
* Downloaded a [book](https://ebookcentral.proquest.com/lib/unican/detail.action?docID=1362587#) through the university's library that explains Cython in-depth

##### Work for next day
* Take a look at the book
* Try to call Numpy's functions without using python types. Starting point [article](https://cython.readthedocs.io/en/latest/src/userguide/numpy_tutorial.html#numpy-tutorial)

### 25/06/2020

##### Work done

* Acomplished to access the Numpy C API through CPython
  * I had some troubles because the headers weren't found by the compiler
  * I had to add a little script to find the path to the Numpy headers and tell the compiler to use them
    * This was a bit tricky because the [documentation](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#configuring-the-c-build) is broken on how to do this
    * I found how to do it in a [github issue](https://github.com/cython/cython/issues/1480)
* Found an [useful flag](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#cythonize-arguments) to generate a report on how much interactions our code have with Python. The ideal would be to drop the number of interactions as much as posible.
* Numpy implements it's own version of the correlation function. For the benchmarks we are gonna our own definition but for the final version we will use it
* After doing some benchmarks, numpy c bindings still have a huge overhead compared to manually implementing the slice operations.

##### Work for next day

* Look for a substitute to Numpy, probably a stablised C library, that minimizes the overhead.

### 01/07/2020

##### Work done

* Found GSL GNU, a C library that implements the necesary primitives for the project
  * Added a benchmark of a GSL version to the autocorrelation version
  * There is a 5.5% speedup from the CPython version
* GSL has it's own overheads that could be tackled with a bare-metal implementation(for example, using raw pointers)
  * There exist more efficient implementations but GSL is a good comparison on complexity vs performance
