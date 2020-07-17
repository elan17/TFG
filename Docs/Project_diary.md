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

* Acomplished to access the Numpy C API through Cython
  * I had some troubles because the headers weren't found by the compiler
  * I had to add a little script to find the path to the Numpy headers and tell the compiler to use them
    * This was a bit tricky because the [documentation](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#configuring-the-c-build) is broken on how to do this
    * I found how to do it in a [github issue](https://github.com/cython/cython/issues/1480)
* Found an [useful flag](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#cythonize-arguments) to generate a report on how much interactions our code have with Python. The ideal would be to drop the number of interactions as much as posible.
* Numpy implements it's own version of the correlation function. For the benchmarks we are gonna use our own definition but for the final version we will use it
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

### 12/07/2020

##### Work done

* After having a meeting with my project director, I am  tasked to look for a way to relate the autocorrelation function of a sequence to the autocorrelation function of a sequence build with the composition method from that sequence
  * As the composition method uses the CRT and the current autocorrelation implementation uses Fourier transforms, the chapter 17 of Manfred's book it's worth to take a look

### 15/07/2020

##### Work done

* After having an idea on how to approach the function from the last session, i started coding the first end project lines
  * The autocorrelation function it's already implemented through Wiener–Khinchin's algorythm
  * The composition function it's already implemented and free from Python's boilerplate in it's loop
  * The optimized autocorrelation function for the composition case is implemented but must be debugged

##### Work for next day

* Fix the composite_autocorrelation function
* Search for a built-in efficient autocorrelation implementation in numpy or scipy
  * From the docs I searched, I'm not sure if it uses the naive approach, the FFT's one or both depending on the size of the problem

### 17/07/2020

##### Work done

* Fixed the composite_autocorrelation function.
  * The % operator have different semantics in C, it represents the remainder operation instead of the module operation
* Started the test suite for the project
  * I decided to approach it with 2 paradigms
    * Property-based testing for pure functions usign [Hypothesis](https://github.com/HypothesisWorks/hypothesis)
    * Harcoded cases for impure functions
* Reestructured repository
* Added the backbone of setup.py to build the project in a modular way
* Added .gitignore files per directory to clean the repository from generated files
