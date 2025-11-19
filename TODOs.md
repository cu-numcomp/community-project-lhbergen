# General 
TODO: matrix generator
We can create a n\*n unitary matrix by generating a n\*n matrix A with random complex entries. Then the sum of A and it's complex conjugate will give a unitary matrix U that we can use as the input to our QR algorithm

## QR from class
##### TODO: update QR 
update the algorithm from class to use complex conjugates instead of transposes so that it works on complex matrices

##### TODO: establish limits
run this updated algorithm without GPU acceleration on random unitary matrices of size n\*n, increasing n each time till we start getting runtimes greater than a few minutes. This will be the upper limit to our size testing

##### TODO: data collection
run this updated algorithm with and without GPU acceleration on random unitary matrices of size 2\*2 to n\*n, logging the runtime.

## New QR
##### TODO: algorithm development
Starting at section 3 of [The Paper](https://arxiv.org/pdf/2004.07710), we should make sure we can program each step starting from EQ4 and ending at EQ11. We should hopefully, at this point, have a functioning algorithm
##### TODO: data collection
run this updated algorithm with and without GPU acceleration on random unitary matrices of size 2\*2 to n\*n, logging the runtime

### TODO: improvement 1
Starting at page 14, we have 3 bulletpoints outlining potential improvements, we should create an updated version of the algorithm as described by the first bulletpoint. 

##### TODO: data collection
run this updated algorithm with and without GPU acceleration on random unitary matrices of size 2\*2 to n\*n, logging the runtime. This is one of the most important because of the claim that this "appears to scale better". I hope to replicate this claim experimentally and the runtimes for this version should scale better than the previous two algorithms

### TODO: improvement 2
Starting at page 14, we have 3 bulletpoints outlining potential improvements, we should create an updated version of the algorithm as described by the first and second bulletpoints.

##### TODO: data collection
run this updated algorithm with and without GPU acceleration on random unitary matrices of size 2\*2 to n\*n, logging the runtime

### TODO: improvement 3
Starting at page 14, we have 3 bulletpoints outlining potential improvements, we should create an updated version of the algorithm as described by all three bulletpoints. This seems like it will be the hardest step, however our code at this point can mirror the pseudo-code on page 15, which will serve as a useful point of reference

##### TODO: data collection
run this updated algorithm with and without GPU acceleration on random unitary matrices of size 2\*2 to n\*n, logging the runtime