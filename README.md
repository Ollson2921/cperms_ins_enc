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
    

## Using cperms_ins_enc

The cperms_ins_enc library uses the comb_spec_searcher module. To find a specification for a set of pattern avoiding Cayley permutations we first create a searcher. There are two different types, one for vertical insertion encoding and one for horizontal insertion encoding.

.. code-block:: python

    >>> from cperms_ins_enc import VerticalSearcher, HorizontalSearcher

Each type can enumerate different classes of Cayley permutations. There is a linear time check in the `check_can_enumerate` file in the `examples` folder to determine if a basis can be enumerated with either type of insertion encoding, where a basis is a string of Cayley permutations.

.. code-block:: python

    >>> basis = "231, 312, 2121"
    >>> print("Can enumerate with vertical insertion encoding:", regular_vertical_insertion_encoding(string_to_basis(basis)))
    >>> print("Can enumerate with horizontal insertion encoding:", regular_horizontal_insertion_encoding(string_to_basis(basis)))
    <!-- Finish the output for this -->

The rest of this README will be an example of using `VerticalSearcher` to enumerate a class. The process is the same for `HorizontalSearcher` but replacing vertical with horizontal throughout.
We initialise `VerticalSearcher` with the basis. 

.. code-block:: python

    >>> basis = "231, 312, 2121"
    >>> searcher = VerticalSearcher(basis)

Calling the auto_search function on `VerticalSearcher` finds the specification for the class.
<!-- If a class can not be enumerated with the type of insertion encoding you are using then this will create an error. -->

.. code-block:: python

    >>> spec = VatterVerticalSearcher(basis).auto_search(max_expansion_time=600)
<!-- Paste the output for a class here -->


The specification returned is a CombinatorialSpecification from the comb_spec_searcher module. To view these you can either print the   specification for a string representation or use the show method to visualise the specification in a proof tree format.

.. code-block:: python

    >>> print(spec)
<!-- Paste the output for a class here -->
    >>> spec.show()
<!-- Paste the output for a class here -->

Any method from CombinatorialSpecification can be used, but in particular the get_genf() function finds the generating function and counts or the counts can be found using the specification as a recurrence up to length `n` for any `n`.

.. code-block:: python

    >>> spec.get_genf()
<!-- Paste the output for a class here -->

    >>> n = 10
    >>> print([specification.count_objects_of_size(i) for i in range(n)])
<!-- Paste the output for a class here -->

