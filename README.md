# CayleyPermutationsInsEnc
CayleyPermutationsInsEnc is a python library for enumerating Cayley permutations with the insertion encoding.

A Cayley permutation is a word $\pi \in \mathbb{N}^*$ such that every number between 1 and the maximum value of $\pi$ appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. 

There are two types of insertion encoding for enumerating Cayley permutations. The vertical insertion encoding inserts new maxima in the Cayley permutation and horizontal insertion encoding inserts new rightmost values.
 
For more information, please see <!-- Link to paper here -->

If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: <!-- https://discord.gg/ -->

Installing
==========

To install cperms_ins_enc on your system, run the following after cloning the repository:

.. code-block:: bash

    ./setup.py

It is also possible to install cperms_ins_enc in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    ./setup.py develop
    

Using cperms_ins_enc
#############

The cperms_ins_enc library uses the comb_spec_searcher module. To find a specification for a set of pattern avoiding Cayley permutations we first create a searcher. There are two different types, one for vertical insertion encoding and one for horizontal insertion encoding.

.. code-block:: python

    >>> from cperms_ins_enc import VerticalSearcher, HorizontalSearcher

Each type can enumerate different classes of Cayley permutations. There is a linear time check in the `examples` folder in `check_can_enumerate`. After inputting the basis for a class you want to enumerate the file will tell you if you can enumerate it with each of the methods, where a basis is a string of Cayley permutations.

.. code-block:: python

    >>> basis = "231, 312, 2121"
    >>> print("Can enumerate with vertical insertion encoding:", regular_vertical_insertion_encoding(string_to_basis(basis)))
    >>> print("Can enumerate with horizontal insertion encoding:", regular_horizontal_insertion_encoding(string_to_basis(basis)))
    <!-- Finish the output for this -->

We will go through an example of using `VerticalSearcher` to enumerate a class, the process is the same for `HorizontalSearcher` but replacing vertical with horizontal throughout.
We initialise `VerticalSearcher` with the basis. 

.. code-block:: python

    >>> basis = "231, 312, 2121"
    >>> searcher = VerticalSearcher(basis)

Calling the `auto_search` function on `VerticalSearcher` finds the specification for the class.

.. code-block:: python

    >>> spec = VatterVerticalSearcher(basis).auto_search(max_expansion_time=600)
<!-- Paste the output for a class here -->

<!-- ### Enumerating Cayley permutation classes

A class can only be enumerated using the insertion encoding if it is regular for that type of insertion encoding.
In the ``examples`` folder, the file ``checking_if_regular`` can be used to check if a basis has a regular vertical or horizontal insertion encoding using a linear time algorithm. If a basis fails both of these checks then it can't be enumerated using the methods in this library.

If a class has a regular vertical insertion encoding then there are two different algorithms for applying the insertion encoding. Examples of each of these can be found in the ``examples`` folder under ``vertical_vatters_method`` and ``vertical_ins_encoding`` respectively. The first of these,  ``vertical_vatters_method``, is an implementation of the vertical insertion encoding by directly extending Vatter's method for enumerating permutation classes using insertion encoding whereas the ``vertical_ins_encoding`` implements vertical insertion encoding using the tilings method.
Based on computational experiments, the tilings method is a faster algorithm so we would recommend following the example in the ``vertical_ins_encoding`` file to enumerate classes with this method.

Tilings are also used to enumerate Cayley permutation classes with the horizontal insertion encoding. An example of this method can be found in the ``horizontal_ins_encoding`` file. 
Each of these three files will raise an error if the input class will not succeed with that method. On a success, they will print the specification, generating function and counts for the class up to length $n$ for some $n$. -->

