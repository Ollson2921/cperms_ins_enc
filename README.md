# CayleyPermutationsInsEnc
This is a python library for enumerating Cayley permutations with the insertion encoding.

## Installing

### Cayley Permutations
A Cayley permutation is a word $\pi \in \mathbb{N}^*$ such that every number between 1 and the maximum value of $\pi$ appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. 

There are two types of insertion encoding for enumerating Cayley permutations. The vertical insertion encoding inserts new maxima in the Cayley permutation and horizontal insertion encoding inserts new rightmost values.
 
For more information, please see...


### Creating a Cayley permutation
The input to a Cayley permutation can be one-based or zero-based and will adjust to being zero-based automatically, but it must be a valid Cayley permutation. It can be initiated with any type of iterable of integers.
Below are some examples of the `CayleyPermutation` class.

.. code-block:: python

    >>> print(CayleyPermutation([]))  # Empty Cayley permutation
    ε
    >>> print(CayleyPermutation((1, 2, 3, 4))) # The Cayley permutation 1234
    0123
    >>> print(CayleyPermutation([0, 1, 2, 3])) # Another way of inputting 1234
    0123

But, `CayleyPermutation((2,3,4,5))` is not a valid Cayley permutation as it is not one-based or zero-based. Similarly, `CayleyPermutation([0,1,3,4])` is not valid as there must be an occurrence of every value between it's minimum and it's maximum. Both of these will raise an error.

A basis is an iterable of Cayley permutations. This can be created directly or using the `string_to_basis` function found in the ``cayley_permutations`` folder which takes as input a string containing Cayley permutations separated by anything and each zero-based or one-based. This function also simplifies the basis by removing any Cayley permutations which are contained in another Cayley permutation in the basis. Some examples are shown below of creating a basis directly and of using the `string_to_basis` function.

.. code-block:: python

    >>> print((CayleyPermutation((0,1,2,3)), CayleyPermutation((1,2,0))))
    (0123, 120)
    >>> print([CayleyPermutation((0,1,2,3)), CayleyPermutation((1,2,0)), CayleyPermutation((4,1,3,0,2))])
    [0123, 120, 41302]
    >>> print(string_to_basis("0123, 231"))
    {0123, 120}
    >>> print(string_to_basis("0123, 231, 41302")) # As 41302 contains 120 it is removed
    {0123, 120}



### Enumerating Cayley permutation classes

A class can only be enumerated using the insertion encoding if it is regular for that type of insertion encoding.
In the ``examples`` folder, the file ``checking_if_regular`` can be used to check if a basis has a regular vertical or horizontal insertion encoding using a linear time algorithm. If a basis fails both of these checks then it can't be enumerated using the methods in this library.

If a class has a regular vertical insertion encoding then there are two different algorithms for applying the insertion encoding. Examples of each of these can be found in the ``examples`` folder under ``vertical_vatters_method`` and ``vertical_ins_encoding`` respectively. The first of these,  ``vertical_vatters_method``, is an implementation of the vertical insertion encoding by directly extending Vatter's method for enumerating permutation classes using insertion encoding whereas the ``vertical_ins_encoding`` implements vertical insertion encoding using the tilings method.
Based on computational experiments, the tilings method is a faster algorithm so we would recommend following the example in the ``vertical_ins_encoding`` file to enumerate classes with this method.

Tilings are also used to enumerate Cayley permutation classes with the horizontal insertion encoding. An example of this method can be found in the ``horizontal_ins_encoding`` file. 
Each of these three files will raise an error if the input class will not succeed with that method. On a success, they will print the specification, generating function and counts for the class up to length $n$ for some $n$.

### Brute force checks

The Cayley permutations in a class can be found by brute force... - should we include this or not?


### Any other useful functions to add?

There is also a file in the examples folder for counting how many classes have a regular insertion encoding of each type, should I take that out too?