# CayleyPermutationsInsEnc
This is a python library for enumerating Cayley permutations with the insertion encoding.

## Installing

### Cayley Permutations
A Cayley permutation is a word $\pi \in \mathbb{N}^*$ such that every number between 1 and the maximum value of $\pi$ appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. 

There are two types of insertion encoding for enumerating Cayley permutations. The vertical insertion encoding inserts new maxima in the Cayley permutation and horizontal insertion encoding inserts new rightmost values.
 
For more information, please see...


### Creating a Cayley permutation
The input to a Cayley permutation can be one-based or zero-based and will adjust to being zero-based automatically, but it must be a valid Cayley permutation. It can also be initiated with any type of iterable of integers.
Below are some examples of the CayleyPermutation class.
.. code-block:: python

    >>> CayleyPermutation([])  # Empty Cayley permutation
    ε
    >>> CayleyPermutation((1, 2, 3, 4)) # The Cayley permutation 1234
    0123
    >>> CayleyPermutation([0, 1, 2, 3]) # Another way of inputting 1234
    0123

But, `CayleyPermutation((2,3,4,5))` is not a valid Cayley permutation as it is not one-based or zero-based. Similarly, `CayleyPermutation([0,1,3,4])` is not valid as there must be an occurrence of every value between it's minimum and it's maximum. Both of these will raise an error.

A basis is an iterable of Cayley permutations. This can be created directly or using the `string_to_basis` function found in the ``cayley_permutations`` folder which takes as input a string containing Cayley permutations separated by anything and each zero-based or one-based. This function also simplifies the basis by removing any Cayley permutations which are contained in another Cayley permutation in the basis. Some examples are shown below.
.. code-block:: python

    >>> string_to_basis("0123, 231")
    {0123, 120}
    >>> string_to_basis("0123, 231, 41302") # As 120 is contained in 41302
    {0123, 120}

### Checking if a class will succeed


In the ``examples`` folder, the file ``checking_if_regular`` can be used to check if a basis has regular insertion encoding for either of the two types.


### Enumerating Cayley permutation classes
There are three diffferent ways to enumerate Cayley permutation classes. Examples of using each of these methods can be found in the ``examples`` folder under ``vertical_vatters_method``, ``vertical_ins_encoding`` and  ``horizontal_ins_encoding``respectively. The first of these,  ``vertical_vatters_method``, is an implementation of the vertical insertion encoding by directly extending Vatter's method for enumerating permutation classes using insertion encoding. The example in ``vertical_ins_encoding`` also uses vertical insertion encoding but is implemented using the tilings method. Tilings are also used for horizontal insertion encoding in the ``horizontal_ins_encoding`` file. 

For each of these files will raise an error if the input class will not succeed with that method. On a success, they will print the specification, generating function and counts for the class up to length $n$ for some $n$.

### Brute force checks