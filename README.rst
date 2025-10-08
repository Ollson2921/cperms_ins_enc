###############################
insertion_encoding
###############################

insertion_encoding is a python library for enumerating Cayley permutations, restricted growth functions and restricted growth functions of (perfect) matchings with the insertion encoding.

A Cayley permutation is a word `π ∈ ℕ*` such that every number between 1 and the maximum value of `π` appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. Cayley permutations are in bijection with ordered set partitions.

Restricted growth functions are a subset of Cayley permutations such that the first occurrence of a value `n` must occur after an occurrence of every value smaller than `n`. They are in bijection with unordered set partitions. Restricted growth functions of matchings are in bijection with unordered set partitions with every block of size 2, so have exactly two occurrences of every value.

There are two types of insertion encoding for enumerating Cayley permutations. The vertical insertion encoding inserts new maxima in the Cayley permutation and horizontal insertion encoding inserts new rightmost values. This library implements both types of insertion encoding for Cayley permutations and restricted growth functions and the horizontal insertion encoding for restricted growth functions of matchings.
 
If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: https://discord.gg/ngPZVT5

==========
Installing
==========

To install insertion_encoding on your system, run the following after cloning the repository:

.. code-block:: bash

    ./setup.py

It is also possible to install insertion_encoding in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    ./setup.py develop
    

========================
Using insertion_encoding
========================

The insertion_encoding module uses the comb_spec_searcher module. To find a specification for a set of pattern avoiding Cayley permutations we first create a searcher. There are five different types:

    - ```VerticalSearcher``` for vertical insertion of Cayley permutations,
    - ```HorizontalSearcher``` for horizontal insertion of Cayley permutations,
    - ```RGFVerticalSearcher``` for vertical insertion of restricted growth functions,
    - ```RGFHorizontalSearcher``` for horizontal insertion of restricted growth functions,
    - ```MatchingHorizontalSearcher``` for horizontal insertion of restricted growth functions of matchings.
For example, the code below shows how to import the two different searchers for enumerating Cayley permutations.

.. code-block:: python

    >>> from insertion_encoding import VerticalSearcher, HorizontalSearcher

Each searcher can enumerate different classes of Cayley permutations. The ```examples``` folder contains a ```cayley_perms``` folder and an ```rgfs``` folder for enumerating the two different types of words. In each folder, the file ``check_can_enumerate`` contains a linear time on the basis to determine if the class avoiding it can be enumerated with either type of insertion encoding, where a basis is a string of Cayley permutations. Below is an example for a class of Cayley permutations.

.. code-block:: python

    >>> from insertion_encoding import regular_vertical_insertion_encoding, regular_horizontal_insertion_encoding

    >>> basis = "231, 312, 2121"
    >>> print("Can enumerate with vertical insertion encoding:", regular_vertical_insertion_encoding(basis))
    >>> print("Can enumerate with horizontal insertion encoding:", regular_horizontal_insertion_encoding(basis))
    Can enumerate with vertical insertion encoding: True
    Can enumerate with horizontal insertion encoding: True

The rest of this README will be an example of using ``VerticalSearcher`` to enumerate the class of hare pop-stack sortable Cayley permutations. The process is the same for any other class by changing the basis and can be done with any of the other searchers by replacing ``VerticalSearcher`` with the appropriate searcher from the list above. 
We initialise ``VerticalSearcher`` with the basis. 

.. code-block:: python

    >>> basis = "231, 312, 2121"
    >>> searcher = VerticalSearcher(basis)

Calling the auto_search function on ``VerticalSearcher`` finds the specification for the class.

.. code-block:: python

    >>> spec = VerticalSearcher(basis).auto_search(max_expansion_time=600)
    [I 250411 11:33:48 comb_spec_searcher:514] Auto search started
    Initialising CombSpecSearcher for the combinatorial class:
    +---+
    | 0 |
    +---+
    Key:
    0: Av(120,201,1010)
    Crossing obstructions:

    Looking for recursive combinatorial specification with the strategies:
    Inferral: Remove empty rows and columns
    Initial: Factor the tiling into factors, Make columns positive
    Verification: verify atoms
    Set 1: Place next point of insertion encoding

    [I 250411 11:33:49 comb_spec_searcher:605] No more classes to expand.
    [I 250411 11:33:49 comb_spec_searcher:553] Specification detected.
    [I 250411 11:33:49 base:306] Minimizing for 0 seconds.
    [I 250411 11:33:49 base:267] Found specification with 16 rules.
    [I 250411 11:33:50 comb_spec_searcher:469] Specification built
        Time taken: 0:00:01
        CSS status:
            Total time accounted for: 0:00:00
                                                        Number of                                Number of
                                                    applications    Time spent    Percentage        rules
            --------------------------------------  --------------  ------------  ------------  -----------
            verify atoms                                        47       0:00:00            0%            2
            Remove empty rows and columns                       32       0:00:00            2%           26
            has specification                                   13       0:00:00            0%            -
            Factor the tiling into factors                      19       0:00:00            2%            5
            Make columns positive                               14       0:00:00            2%            8
            add rule                                            47       0:00:00            0%            -
            Place next point of insertion encoding               6       0:00:00           92%            6

        ClassDB status:
            Total number of combinatorial classes found is 54
            is_empty check applied 28 time. Time spent: 0:00:00
        Queue status (currently on level 4):
            Queue              Size
            ---------------  ------
            working               0
            current (set 1)       0
            next                  0
            The size of the current queues at each level: 2, 5, 11, 5
        RuleDB status:
                                                    Total number
            ---------------------------------------  --------------
            Combinatorial rules                                  16
            Equivalence rules                                    31
            Combintorial rules up to equivalence                 16
            Strategy verified combinatorial classes               2
            Verified combinatorial classes                       16
            combinatorial classes up to equivalence              16
            Called find equiv path 13 times, for total time of 0.0 seconds.

        Memory Status:
            ------------  --------
            OS Allocated  66.8 MiB
            CSS            354 KiB
            ClassDB        296 KiB
            ClassQueue      11 KiB
            RuleDB         354 KiB
            ------------  --------
        Specification found has 43 rules


The specification returned is a ``CombinatorialSpecification`` from the comb_spec_searcher module. To view these you can either print the   specification for a string representation or use the show method to visualise the specification in a proof tree format.

.. code-block:: python

    >>> print(spec)
    A combinatorial specification with 43 rules.
    -----------
    0 -> (1, 3)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 0),))})
    +---+                       +---+                       +---+
    | 0 |                    =  | # |                    +  | 0 |
    +---+                       +---+                       +---+
    Key:                        Key:                        Key:
    0: Av(120,201,1010)         Crossing obstructions:      0: Av(120,201,1010)
    Crossing obstructions:                                  Crossing obstructions:
                                                            Requirements 0:
                                                            0: ((0, 0))

    -----
    1 = 2
    Remove empty rows and columns
    +---+                       +---+
    | # |                    =  | # |
    +---+                       +---+
    Key:                        Dimensions (0, 0)
    Crossing obstructions:      Key:
                                Crossing obstructions:
    -------
    2 -> ()
    is atom
    +---+
    | # |
    +---+
    Dimensions (0, 0)
    Key:
    Crossing obstructions:
    -----
    3 = 4
    Placed the point of the requirement (GriddedCayleyPerm(0, ((0, 0),)),) at indices (0,) in direction 4 but only child and index 1 is non-empty, then Remove empty rows and columns
    +---+                       +---+---+---+                           +---+---+---+
    | 0 |                    =  | 0 | # | 2 |                        =  | 0 | # | 2 |
    +---+                       +---+---+---+                           +---+---+---+
    Key:                        | # | ● | 1 |                           | # | ● | 1 |
    0: Av(120,201,1010)         +---+---+---+                           +---+---+---+
    Crossing obstructions:      | # | # | # |                           Key:
    Requirements 0:             +---+---+---+                           0: Av(01)
    0: ((0, 0))                 Key:                                    1: Av(01,10)
                                0: Av(01)                               2: Av(120,201,1010)
                                1: Av(01,10)                            Crossing obstructions:
                                2: Av(120,201,1010)                     01: ((1, 0),(2, 0))
                                Crossing obstructions:                  10: ((0, 1),(2, 1))
                                01: ((1, 1),(2, 1))                     10: ((1, 0),(2, 0))
                                10: ((0, 2),(2, 2))                     110: ((0, 1),(2, 1),(2, 0))
                                10: ((1, 1),(2, 1))                     120: ((0, 1),(2, 1),(2, 0))
                                110: ((0, 2),(2, 2),(2, 1))             120: ((2, 1),(2, 1),(2, 0))
                                120: ((0, 2),(2, 2),(2, 1))             201: ((2, 1),(2, 0),(2, 1))
                                120: ((2, 2),(2, 2),(2, 1))             1010: ((2, 1),(2, 0),(2, 1),(2, 0))
                                201: ((2, 2),(2, 1),(2, 2))             Requirements 0:
                                1010: ((2, 2),(2, 1),(2, 2),(2, 1))     0: ((1, 0))
                                Requirements 0:
                                0: ((1, 1))

    ------------
    4 -> (5, 20)
    Factor the tiling into factors
    +---+---+---+                           +---+---+---+                           +---+---+---+
    | 0 | # | 2 |                        =  | 0 | # | 2 |                        x  | # | # | # |
    +---+---+---+                           +---+---+---+                           +---+---+---+
    | # | ● | 1 |                           | # | # | 1 |                           | # | ● | # |
    +---+---+---+                           +---+---+---+                           +---+---+---+
    Key:                                    Key:                                    Key:
    0: Av(01)                               0: Av(01)                               Crossing obstructions:
    1: Av(01,10)                            1: Av(01,10)                            Requirements 0:
    2: Av(120,201,1010)                     2: Av(120,201,1010)                     0: ((1, 0))
    Crossing obstructions:                  Crossing obstructions:
    01: ((1, 0),(2, 0))                     10: ((0, 1),(2, 1))
    10: ((0, 1),(2, 1))                     110: ((0, 1),(2, 1),(2, 0))
    10: ((1, 0),(2, 0))                     120: ((0, 1),(2, 1),(2, 0))
    110: ((0, 1),(2, 1),(2, 0))             120: ((2, 1),(2, 1),(2, 0))
    120: ((0, 1),(2, 1),(2, 0))             201: ((2, 1),(2, 0),(2, 1))
    120: ((2, 1),(2, 1),(2, 0))             1010: ((2, 1),(2, 0),(2, 1),(2, 0))
    201: ((2, 1),(2, 0),(2, 1))
    1010: ((2, 1),(2, 0),(2, 1),(2, 0))
    Requirements 0:
    0: ((1, 0))

    -----
    5 = 6
    Remove empty rows and columns
    +---+---+---+                           +---+---+
    | 0 | # | 2 |                        =  | 0 | 2 |
    +---+---+---+                           +---+---+
    | # | # | 1 |                           | # | 1 |
    +---+---+---+                           +---+---+
    Key:                                    Key:
    0: Av(01)                               0: Av(01)
    1: Av(01,10)                            1: Av(01,10)
    2: Av(120,201,1010)                     2: Av(120,201,1010)
    Crossing obstructions:                  Crossing obstructions:
    10: ((0, 1),(2, 1))                     10: ((0, 1),(1, 1))
    110: ((0, 1),(2, 1),(2, 0))             110: ((0, 1),(1, 1),(1, 0))
    120: ((0, 1),(2, 1),(2, 0))             120: ((0, 1),(1, 1),(1, 0))
    120: ((2, 1),(2, 1),(2, 0))             120: ((1, 1),(1, 1),(1, 0))
    201: ((2, 1),(2, 0),(2, 1))             201: ((1, 1),(1, 0),(1, 1))
    1010: ((2, 1),(2, 0),(2, 1),(2, 0))     1010: ((1, 1),(1, 0),(1, 1),(1, 0))

    ------------
    6 -> (7, 14)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 1),))})
    +---+---+                               +---+---+                               +---+---+
    | 0 | 2 |                            =  | # | 1 |                            +  | 0 | 2 |
    +---+---+                               +---+---+                               +---+---+
    | # | 1 |                               | # | 0 |                               | # | 1 |
    +---+---+                               +---+---+                               +---+---+
    Key:                                    Key:                                    Key:
    0: Av(01)                               0: Av(01,10)                            0: Av(01)
    1: Av(01,10)                            1: Av(120,201,1010)                     1: Av(01,10)
    2: Av(120,201,1010)                     Crossing obstructions:                  2: Av(120,201,1010)
    Crossing obstructions:                  120: ((1, 1),(1, 1),(1, 0))             Crossing obstructions:
    10: ((0, 1),(1, 1))                     201: ((1, 1),(1, 0),(1, 1))             10: ((0, 1),(1, 1))
    110: ((0, 1),(1, 1),(1, 0))             1010: ((1, 1),(1, 0),(1, 1),(1, 0))     110: ((0, 1),(1, 1),(1, 0))
    120: ((0, 1),(1, 1),(1, 0))                                                     120: ((0, 1),(1, 1),(1, 0))
    120: ((1, 1),(1, 1),(1, 0))                                                     120: ((1, 1),(1, 1),(1, 0))
    201: ((1, 1),(1, 0),(1, 1))                                                     201: ((1, 1),(1, 0),(1, 1))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))                                             1010: ((1, 1),(1, 0),(1, 1),(1, 0))
                                                                                    Requirements 0:
                                                                                    0: ((0, 1))

    -----
    7 = 8
    Remove empty rows and columns
    +---+---+                               +---+
    | # | 1 |                            =  | 1 |
    +---+---+                               +---+
    | # | 0 |                               | 0 |
    +---+---+                               +---+
    Key:                                    Key:
    0: Av(01,10)                            0: Av(01,10)
    1: Av(120,201,1010)                     1: Av(120,201,1010)
    Crossing obstructions:                  Crossing obstructions:
    120: ((1, 1),(1, 1),(1, 0))             120: ((0, 1),(0, 1),(0, 0))
    201: ((1, 1),(1, 0),(1, 1))             201: ((0, 1),(0, 0),(0, 1))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))     1010: ((0, 1),(0, 0),(0, 1),(0, 0))

    ------------
    8 -> (9, 10)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 1),)), GriddedCayleyPerm(0, ((0, 0),))})
    +---+                                   +---+                       +---+
    | 1 |                                =  | # |                    +  | 1 |
    +---+                                   +---+                       +---+
    | 0 |                                   | # |                       | 0 |
    +---+                                   +---+                       +---+
    Key:                                    Key:                        Key:
    0: Av(01,10)                            Crossing obstructions:      0: Av(01,10)
    1: Av(120,201,1010)                                                 1: Av(120,201,1010)
    Crossing obstructions:                                              Crossing obstructions:
    120: ((0, 1),(0, 1),(0, 0))                                         120: ((0, 1),(0, 1),(0, 0))
    201: ((0, 1),(0, 0),(0, 1))                                         201: ((0, 1),(0, 0),(0, 1))
    1010: ((0, 1),(0, 0),(0, 1),(0, 0))                                 1010: ((0, 1),(0, 0),(0, 1),(0, 0))
                                                                        Requirements 0:
                                                                        0: ((0, 0))
                                                                        0: ((0, 1))

    -----
    9 = 2
    Remove empty rows and columns
    +---+                       +---+
    | # |                    =  | # |
    +---+                       +---+
    | # |                       Dimensions (0, 0)
    +---+                       Key:
    Key:                        Crossing obstructions:
    Crossing obstructions:

    ------------------
    10 -> (11, 12, 13)
    Placed the point of the requirement (GriddedCayleyPerm(0, ((0, 1),)), GriddedCayleyPerm(0, ((0, 0),))) at indices (0, 0) in direction 4
    +---+                                   +---+                       +---+---+---+                           +---+---+---+
    | 1 |                                =  | ∅ |                    +  | 0 | # | 2 |                        +  | 0 | # | 2 |
    +---+                                   +---+                       +---+---+---+                           +---+---+---+
    | 0 |                                   | ∅ |                       | # | # | # |                           | # | ● | 1 |
    +---+                                   +---+                       +---+---+---+                           +---+---+---+
    Key:                                    Key:                        | # | ● | 1 |                           | # | # | # |
    0: Av(01,10)                            ∅: Av(ε)                    +---+---+---+                           +---+---+---+
    1: Av(120,201,1010)                     Crossing obstructions:      | # | # | # |                           | # | # | # |
    Crossing obstructions:                  Requirements 0:             +---+---+---+                           +---+---+---+
    120: ((0, 1),(0, 1),(0, 0))                                         Key:                                    Key:        
    201: ((0, 1),(0, 0),(0, 1))                                         0: Av(01)                               0: Av(01)   
    1010: ((0, 1),(0, 0),(0, 1),(0, 0))                                 1: Av(01,10)                            1: Av(01,10)
    Requirements 0:                                                     2: Av(120,201,1010)                     2: Av(120,201,1010)
    0: ((0, 0))                                                         Crossing obstructions:                  Crossing obstructions:
    0: ((0, 1))                                                         01: ((1, 1),(2, 1))                     01: ((1, 2),(2, 2))
                                                                        10: ((0, 3),(2, 3))                     10: ((0, 3),(2, 3))
                                                                        10: ((1, 1),(2, 1))                     10: ((1, 2),(2, 2))
                                                                        110: ((0, 3),(2, 3),(2, 1))             110: ((0, 3),(2, 3),(2, 2))
                                                                        120: ((0, 3),(2, 3),(2, 1))             120: ((0, 3),(2, 3),(2, 2))
                                                                        120: ((2, 3),(2, 3),(2, 1))             120: ((2, 3),(2, 3),(2, 2))
                                                                        201: ((2, 3),(2, 1),(2, 3))             201: ((2, 3),(2, 2),(2, 3))
                                                                        1010: ((2, 3),(2, 1),(2, 3),(2, 1))     1010: ((2, 3),(2, 2),(2, 3),(2, 2))
                                                                        Requirements 0:                         Requirements 0:
                                                                        0: ((1, 1))                             0: ((1, 2)) 
                                                                                                                            
    --------
    11 -> ()
    is empty
    +---+
    | ∅ |
    +---+
    | ∅ |
    +---+
    Key:
    ∅: Av(ε)
    Crossing obstructions:
    Requirements 0:

    ------
    12 = 4
    Remove empty rows and columns
    +---+---+---+                           +---+---+---+
    | 0 | # | 2 |                        =  | 0 | # | 2 |
    +---+---+---+                           +---+---+---+
    | # | # | # |                           | # | ● | 1 |
    +---+---+---+                           +---+---+---+
    | # | ● | 1 |                           Key:
    +---+---+---+                           0: Av(01)
    | # | # | # |                           1: Av(01,10)
    +---+---+---+                           2: Av(120,201,1010)
    Key:                                    Crossing obstructions:
    0: Av(01)                               01: ((1, 0),(2, 0))
    1: Av(01,10)                            10: ((0, 1),(2, 1))
    2: Av(120,201,1010)                     10: ((1, 0),(2, 0))
    Crossing obstructions:                  110: ((0, 1),(2, 1),(2, 0))
    01: ((1, 1),(2, 1))                     120: ((0, 1),(2, 1),(2, 0))
    10: ((0, 3),(2, 3))                     120: ((2, 1),(2, 1),(2, 0))
    10: ((1, 1),(2, 1))                     201: ((2, 1),(2, 0),(2, 1))
    110: ((0, 3),(2, 3),(2, 1))             1010: ((2, 1),(2, 0),(2, 1),(2, 0))
    120: ((0, 3),(2, 3),(2, 1))             Requirements 0:
    120: ((2, 3),(2, 3),(2, 1))             0: ((1, 0))
    201: ((2, 3),(2, 1),(2, 3))
    1010: ((2, 3),(2, 1),(2, 3),(2, 1))
    Requirements 0:
    0: ((1, 1))

    ------
    13 = 4
    Remove empty rows and columns
    +---+---+---+                           +---+---+---+
    | 0 | # | 2 |                        =  | 0 | # | 2 |
    +---+---+---+                           +---+---+---+
    | # | ● | 1 |                           | # | ● | 1 |
    +---+---+---+                           +---+---+---+
    | # | # | # |                           Key:
    +---+---+---+                           0: Av(01)
    | # | # | # |                           1: Av(01,10)
    +---+---+---+                           2: Av(120,201,1010)
    Key:                                    Crossing obstructions:
    0: Av(01)                               01: ((1, 0),(2, 0))
    1: Av(01,10)                            10: ((0, 1),(2, 1))
    2: Av(120,201,1010)                     10: ((1, 0),(2, 0))
    Crossing obstructions:                  110: ((0, 1),(2, 1),(2, 0))
    01: ((1, 2),(2, 2))                     120: ((0, 1),(2, 1),(2, 0))
    10: ((0, 3),(2, 3))                     120: ((2, 1),(2, 1),(2, 0))
    10: ((1, 2),(2, 2))                     201: ((2, 1),(2, 0),(2, 1))
    110: ((0, 3),(2, 3),(2, 2))             1010: ((2, 1),(2, 0),(2, 1),(2, 0))
    120: ((0, 3),(2, 3),(2, 2))             Requirements 0:
    120: ((2, 3),(2, 3),(2, 2))             0: ((1, 0))
    201: ((2, 3),(2, 2),(2, 3))
    1010: ((2, 3),(2, 2),(2, 3),(2, 2))
    Requirements 0:
    0: ((1, 2))

    --------------
    14 -> (15, 28)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((1, 1),)), GriddedCayleyPerm(0, ((1, 0),))})
    +---+---+                               +---+---+                   +---+---+
    | 0 | 2 |                            =  | 0 | # |                +  | 0 | 2 |
    +---+---+                               +---+---+                   +---+---+
    | # | 1 |                               | # | # |                   | # | 1 |
    +---+---+                               +---+---+                   +---+---+
    Key:                                    Key:                        Key:
    0: Av(01)                               0: Av(01)                   0: Av(01)
    1: Av(01,10)                            Crossing obstructions:      1: Av(01,10)
    2: Av(120,201,1010)                     Requirements 0:             2: Av(120,201,1010)
    Crossing obstructions:                  0: ((0, 1))                 Crossing obstructions:
    10: ((0, 1),(1, 1))                                                 10: ((0, 1),(1, 1))
    110: ((0, 1),(1, 1),(1, 0))                                         110: ((0, 1),(1, 1),(1, 0))
    120: ((0, 1),(1, 1),(1, 0))                                         120: ((0, 1),(1, 1),(1, 0))
    120: ((1, 1),(1, 1),(1, 0))                                         120: ((1, 1),(1, 1),(1, 0))
    201: ((1, 1),(1, 0),(1, 1))                                         201: ((1, 1),(1, 0),(1, 1))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))                                 1010: ((1, 1),(1, 0),(1, 1),(1, 0))
    Requirements 0:                                                     Requirements 0:
    0: ((0, 1))                                                         0: ((0, 1))
                                                                        Requirements 1:
                                                                        0: ((1, 0))
                                                                        0: ((1, 1))

    -------
    15 = 16
    Remove empty rows and columns
    +---+---+                   +---+
    | 0 | # |                =  | 0 |
    +---+---+                   +---+
    | # | # |                   Key:
    +---+---+                   0: Av(01)
    Key:                        Crossing obstructions:
    0: Av(01)                   Requirements 0:
    Crossing obstructions:      0: ((0, 0))
    Requirements 0:
    0: ((0, 1))

    -----------
    16 -> (17,)
    Placed the point of the requirement (GriddedCayleyPerm(0, ((0, 0),)),) at indices (0,) in direction 4 but only child and index 1 is non-empty, then Remove empty rows and columns
    +---+                       +---+---+---+               +---+---+---+
    | 0 |                    =  | 0 | # | # |            =  | 0 | # | # |
    +---+                       +---+---+---+               +---+---+---+
    Key:                        | # | ● | 1 |               | # | ● | 1 |
    0: Av(01)                   +---+---+---+               +---+---+---+
    Crossing obstructions:      | # | # | # |               Key:
    Requirements 0:             +---+---+---+               0: Av(01)
    0: ((0, 0))                 Key:                        1: Av(01,10)
                                0: Av(01)                   Crossing obstructions:
                                1: Av(01,10)                01: ((1, 0),(2, 0))
                                Crossing obstructions:      10: ((1, 0),(2, 0))
                                01: ((1, 1),(2, 1))         Requirements 0:
                                10: ((1, 1),(2, 1))         0: ((1, 0))
                                Requirements 0:
                                0: ((1, 1))

    ------------------
    17 -> (18, 20, 22)
    Factor the tiling into factors
    +---+---+---+               +---+---+---+               +---+---+---+               +---+---+---+
    | 0 | # | # |            =  | 0 | # | # |            x  | # | # | # |            x  | # | # | # |
    +---+---+---+               +---+---+---+               +---+---+---+               +---+---+---+
    | # | ● | 1 |               | # | # | # |               | # | ● | # |               | # | # | 0 |
    +---+---+---+               +---+---+---+               +---+---+---+               +---+---+---+
    Key:                        Key:                        Key:                        Key:
    0: Av(01)                   0: Av(01)                   Crossing obstructions:      0: Av(01,10)
    1: Av(01,10)                Crossing obstructions:      Requirements 0:             Crossing obstructions:
    Crossing obstructions:                                  0: ((1, 0))
    01: ((1, 0),(2, 0))
    10: ((1, 0),(2, 0))
    Requirements 0:
    0: ((1, 0))

    -------
    18 = 19
    Remove empty rows and columns
    +---+---+---+               +---+
    | 0 | # | # |            =  | 0 |
    +---+---+---+               +---+
    | # | # | # |               Key:
    +---+---+---+               0: Av(01)
    Key:                        Crossing obstructions:
    0: Av(01)
    Crossing obstructions:

    -------------
    19 -> (1, 16)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 0),))})
    +---+                       +---+                       +---+
    | 0 |                    =  | # |                    +  | 0 |
    +---+                       +---+                       +---+
    Key:                        Key:                        Key:
    0: Av(01)                   Crossing obstructions:      0: Av(01)
    Crossing obstructions:                                  Crossing obstructions:
                                                            Requirements 0:
                                                            0: ((0, 0))

    -------
    20 = 21
    Remove empty rows and columns
    +---+---+---+               +---+
    | # | # | # |            =  | ● |
    +---+---+---+               +---+
    | # | ● | # |               Key:
    +---+---+---+               Crossing obstructions:
    Key:                        Requirements 0:
    Crossing obstructions:      0: ((0, 0))
    Requirements 0:
    0: ((1, 0))

    --------
    21 -> ()
    is atom
    +---+
    | ● |
    +---+
    Key:
    Crossing obstructions:
    Requirements 0:
    0: ((0, 0))

    -------
    22 = 23
    Remove empty rows and columns
    +---+---+---+               +---+
    | # | # | # |            =  | 0 |
    +---+---+---+               +---+
    | # | # | 0 |               Key:
    +---+---+---+               0: Av(01,10)
    Key:                        Crossing obstructions:
    0: Av(01,10)
    Crossing obstructions:

    -------------
    23 -> (1, 24)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 0),))})
    +---+                       +---+                       +---+
    | 0 |                    =  | # |                    +  | 0 |
    +---+                       +---+                       +---+
    Key:                        Key:                        Key:
    0: Av(01,10)                Crossing obstructions:      0: Av(01,10)
    Crossing obstructions:                                  Crossing obstructions:
                                                            Requirements 0:
                                                            0: ((0, 0))

    -------
    24 = 25
    Placed the point of the requirement (GriddedCayleyPerm(0, ((0, 0),)),) at indices (0,) in direction 4 but only child and index 1 is non-empty, then Remove empty rows and columns
    +---+                       +---+---+---+               +---+---+
    | 0 |                    =  | # | # | # |            =  | ● | 0 |
    +---+                       +---+---+---+               +---+---+
    Key:                        | # | ● | 0 |               Key:
    0: Av(01,10)                +---+---+---+               0: Av(01,10)
    Crossing obstructions:      | # | # | # |               Crossing obstructions:
    Requirements 0:             +---+---+---+               01: ((0, 0),(1, 0))
    0: ((0, 0))                 Key:                        10: ((0, 0),(1, 0))
                                0: Av(01,10)                Requirements 0:
                                Crossing obstructions:      0: ((0, 0))
                                01: ((1, 1),(2, 1))
                                10: ((1, 1),(2, 1))
                                Requirements 0:
                                0: ((1, 1))

    --------------
    25 -> (26, 27)
    Factor the tiling into factors
    +---+---+                   +---+---+                   +---+---+
    | ● | 0 |                =  | ● | # |                x  | # | 0 |
    +---+---+                   +---+---+                   +---+---+
    Key:                        Key:                        Key:
    0: Av(01,10)                Crossing obstructions:      0: Av(01,10)
    Crossing obstructions:      Requirements 0:             Crossing obstructions:
    01: ((0, 0),(1, 0))         0: ((0, 0))
    10: ((0, 0),(1, 0))
    Requirements 0:
    0: ((0, 0))

    -------
    26 = 21
    Remove empty rows and columns
    +---+---+                   +---+
    | ● | # |                =  | ● |
    +---+---+                   +---+
    Key:                        Key:
    Crossing obstructions:      Crossing obstructions:
    Requirements 0:             Requirements 0:
    0: ((0, 0))                 0: ((0, 0))

    -------
    27 = 23
    Remove empty rows and columns
    +---+---+                   +---+
    | # | 0 |                =  | 0 |
    +---+---+                   +---+
    Key:                        Key:
    0: Av(01,10)                0: Av(01,10)
    Crossing obstructions:      Crossing obstructions:

    ----------------------
    28 -> (29, 30, 38, 42)
    Placed the point of the requirement (GriddedCayleyPerm(0, ((0, 1),)), GriddedCayleyPerm(0, ((1, 0),)), GriddedCayleyPerm(0, ((1, 1),))) at indices (0, 0, 0) in direction 4
    +---+---+                               +---+---+                   +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    | 0 | 2 |                            =  | ∅ | ∅ |                +  | 0 | # | # | 2 |                    +  | 0 | 0 | # | 2 |                    +  | ∅ | ∅ | ∅ | ∅ |
    +---+---+                               +---+---+                   +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    | # | 1 |                               | ∅ | ∅ |                   | # | ● | 1 | 1 |                       | # | # | # | # |                       | ∅ | ∅ | ∅ | ∅ |
    +---+---+                               +---+---+                   +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    Key:                                    Key:                        | # | # | # | # |                       | # | # | ● | 1 |                       | ∅ | ∅ | ∅ | ∅ |
    0: Av(01)                               ∅: Av(ε)                    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    1: Av(01,10)                            Crossing obstructions:      | # | # | # | # |                       | # | # | # | # |                       | ∅ | ∅ | ∅ | ∅ |
    2: Av(120,201,1010)                     Requirements 0:             +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    Crossing obstructions:                                              Key:                                    Key:                                    Key:
    10: ((0, 1),(1, 1))                                                 0: Av(01)                               0: Av(01)                               ∅: Av(ε)
    110: ((0, 1),(1, 1),(1, 0))                                         1: Av(01,10)                            1: Av(01,10)                            Crossing obstructions:
    120: ((0, 1),(1, 1),(1, 0))                                         2: Av(120,201,1010)                     2: Av(120,201,1010)                     Requirements 0:
    120: ((1, 1),(1, 1),(1, 0))                                         Crossing obstructions:                  Crossing obstructions:
    201: ((1, 1),(1, 0),(1, 1))                                         01: ((1, 2),(2, 2))                     00: ((0, 3),(1, 3))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))                                 01: ((1, 2),(3, 2))                     01: ((0, 3),(1, 3))
    Requirements 0:                                                     01: ((2, 2),(3, 2))                     01: ((2, 1),(3, 1))
    0: ((0, 1))                                                         10: ((0, 3),(3, 2))                     10: ((0, 3),(1, 3))
    Requirements 1:                                                     10: ((0, 3),(3, 3))                     10: ((0, 3),(3, 3))
    0: ((1, 0))                                                         10: ((1, 2),(2, 2))                     10: ((1, 3),(3, 3))
    0: ((1, 1))                                                         10: ((1, 2),(3, 2))                     10: ((2, 1),(3, 1))
                                                                        10: ((2, 2),(3, 2))                     110: ((0, 3),(3, 3),(3, 1))
                                                                        120: ((3, 3),(3, 3),(3, 2))             110: ((1, 3),(3, 3),(3, 1))
                                                                        201: ((3, 3),(3, 2),(3, 3))             120: ((0, 3),(3, 3),(3, 1))
                                                                        1010: ((3, 3),(3, 2),(3, 3),(3, 2))     120: ((1, 3),(3, 3),(3, 1))
                                                                        Requirements 0:                         120: ((3, 3),(3, 3),(3, 1))
                                                                        0: ((1, 2))                             201: ((3, 3),(3, 1),(3, 3))
                                                                        Requirements 1:                         1010: ((3, 3),(3, 1),(3, 3),(3, 1))
                                                                        0: ((3, 2))                             Requirements 0:
                                                                        0: ((3, 3))                             0: ((0, 3)) 
                                                                                                                Requirements 1:
                                                                                                                0: ((2, 1)) 
                                                                                                                            
    --------
    29 -> ()
    is empty
    +---+---+
    | ∅ | ∅ |
    +---+---+
    | ∅ | ∅ |
    +---+---+
    Key:
    ∅: Av(ε)
    Crossing obstructions:
    Requirements 0:

    -------
    30 = 31
    Remove empty rows and columns
    +---+---+---+---+                       +---+---+---+---+
    | 0 | # | # | 2 |                    =  | 0 | # | # | 2 |
    +---+---+---+---+                       +---+---+---+---+
    | # | ● | 1 | 1 |                       | # | ● | 1 | 1 |
    +---+---+---+---+                       +---+---+---+---+
    | # | # | # | # |                       Key:
    +---+---+---+---+                       0: Av(01)
    | # | # | # | # |                       1: Av(01,10)
    +---+---+---+---+                       2: Av(120,201,1010)
    Key:                                    Crossing obstructions:
    0: Av(01)                               01: ((1, 0),(2, 0))
    1: Av(01,10)                            01: ((1, 0),(3, 0))
    2: Av(120,201,1010)                     01: ((2, 0),(3, 0))
    Crossing obstructions:                  10: ((0, 1),(3, 0))
    01: ((1, 2),(2, 2))                     10: ((0, 1),(3, 1))
    01: ((1, 2),(3, 2))                     10: ((1, 0),(2, 0))
    01: ((2, 2),(3, 2))                     10: ((1, 0),(3, 0))
    10: ((0, 3),(3, 2))                     10: ((2, 0),(3, 0))
    10: ((0, 3),(3, 3))                     120: ((3, 1),(3, 1),(3, 0))
    10: ((1, 2),(2, 2))                     201: ((3, 1),(3, 0),(3, 1))
    10: ((1, 2),(3, 2))                     1010: ((3, 1),(3, 0),(3, 1),(3, 0))
    10: ((2, 2),(3, 2))                     Requirements 0:
    120: ((3, 3),(3, 3),(3, 2))             0: ((1, 0))
    201: ((3, 3),(3, 2),(3, 3))             Requirements 1:
    1010: ((3, 3),(3, 2),(3, 3),(3, 2))     0: ((3, 0))
    Requirements 0:                         0: ((3, 1))
    0: ((1, 2))
    Requirements 1:
    0: ((3, 2))
    0: ((3, 3))

    ------------------
    31 -> (32, 36, 37)
    Factor the tiling into factors
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+           +---+---+---+---+
    | 0 | # | # | 2 |                    =  | 0 | # | # | 2 |                    x  | # | # | # | # |        x  | # | # | # | # |
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+           +---+---+---+---+
    | # | ● | 1 | 1 |                       | # | # | # | 1 |                       | # | ● | # | # |           | # | # | 0 | # |
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+           +---+---+---+---+
    Key:                                    Key:                                    Key:                        Key:        
    0: Av(01)                               0: Av(01)                               Crossing obstructions:      0: Av(01,10)
    1: Av(01,10)                            1: Av(01,10)                            Requirements 0:             Crossing obstructions:
    2: Av(120,201,1010)                     2: Av(120,201,1010)                     0: ((1, 0))                             
    Crossing obstructions:                  Crossing obstructions:
    01: ((1, 0),(2, 0))                     10: ((0, 1),(3, 0))
    01: ((1, 0),(3, 0))                     10: ((0, 1),(3, 1))
    01: ((2, 0),(3, 0))                     120: ((3, 1),(3, 1),(3, 0))
    10: ((0, 1),(3, 0))                     201: ((3, 1),(3, 0),(3, 1))
    10: ((0, 1),(3, 1))                     1010: ((3, 1),(3, 0),(3, 1),(3, 0))
    10: ((1, 0),(2, 0))                     Requirements 0:
    10: ((1, 0),(3, 0))                     0: ((3, 0))
    10: ((2, 0),(3, 0))                     0: ((3, 1))
    120: ((3, 1),(3, 1),(3, 0))
    201: ((3, 1),(3, 0),(3, 1))
    1010: ((3, 1),(3, 0),(3, 1),(3, 0))
    Requirements 0:
    0: ((1, 0))
    Requirements 1:
    0: ((3, 0))
    0: ((3, 1))

    -------
    32 = 33
    Remove empty rows and columns
    +---+---+---+---+                       +---+---+
    | 0 | # | # | 2 |                    =  | 0 | 2 |
    +---+---+---+---+                       +---+---+
    | # | # | # | 1 |                       | # | 1 |
    +---+---+---+---+                       +---+---+
    Key:                                    Key:
    0: Av(01)                               0: Av(01)
    1: Av(01,10)                            1: Av(01,10)
    2: Av(120,201,1010)                     2: Av(120,201,1010)
    Crossing obstructions:                  Crossing obstructions:
    10: ((0, 1),(3, 0))                     10: ((0, 1),(1, 0))
    10: ((0, 1),(3, 1))                     10: ((0, 1),(1, 1))
    120: ((3, 1),(3, 1),(3, 0))             120: ((1, 1),(1, 1),(1, 0))
    201: ((3, 1),(3, 0),(3, 1))             201: ((1, 1),(1, 0),(1, 1))
    1010: ((3, 1),(3, 0),(3, 1),(3, 0))     1010: ((1, 1),(1, 0),(1, 1),(1, 0))
    Requirements 0:                         Requirements 0:
    0: ((3, 0))                             0: ((1, 0))
    0: ((3, 1))                             0: ((1, 1))

    --------------
    33 -> (34, 35)
    Either avoid or contain frozenset({GriddedCayleyPerm(0, ((0, 1),))})
    +---+---+                               +---+---+                               +---+---+
    | 0 | 2 |                            =  | # | 1 |                            +  | 0 | 1 |
    +---+---+                               +---+---+                               +---+---+
    | # | 1 |                               | # | 0 |                               | # | # |
    +---+---+                               +---+---+                               +---+---+
    Key:                                    Key:                                    Key:
    0: Av(01)                               0: Av(01,10)                            0: Av(01)
    1: Av(01,10)                            1: Av(120,201,1010)                     1: Av(120,201,1010)
    2: Av(120,201,1010)                     Crossing obstructions:                  Crossing obstructions:
    Crossing obstructions:                  120: ((1, 1),(1, 1),(1, 0))             10: ((0, 1),(1, 1))
    10: ((0, 1),(1, 0))                     201: ((1, 1),(1, 0),(1, 1))             Requirements 0:
    10: ((0, 1),(1, 1))                     1010: ((1, 1),(1, 0),(1, 1),(1, 0))     0: ((0, 1))
    120: ((1, 1),(1, 1),(1, 0))             Requirements 0:                         Requirements 1:
    201: ((1, 1),(1, 0),(1, 1))             0: ((1, 0))                             0: ((1, 1))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))     0: ((1, 1))
    Requirements 0:
    0: ((1, 0))
    0: ((1, 1))

    -------
    34 = 10
    Remove empty rows and columns
    +---+---+                               +---+
    | # | 1 |                            =  | 1 |
    +---+---+                               +---+
    | # | 0 |                               | 0 |
    +---+---+                               +---+
    Key:                                    Key:
    0: Av(01,10)                            0: Av(01,10)
    1: Av(120,201,1010)                     1: Av(120,201,1010)
    Crossing obstructions:                  Crossing obstructions:
    120: ((1, 1),(1, 1),(1, 0))             120: ((0, 1),(0, 1),(0, 0))
    201: ((1, 1),(1, 0),(1, 1))             201: ((0, 1),(0, 0),(0, 1))
    1010: ((1, 1),(1, 0),(1, 1),(1, 0))     1010: ((0, 1),(0, 0),(0, 1),(0, 0))
    Requirements 0:                         Requirements 0:
    0: ((1, 0))                             0: ((0, 0))
    0: ((1, 1))                             0: ((0, 1))

    -------
    35 = 31
    Remove empty rows and columns, then Placed the point of the requirement (GriddedCayleyPerm(0, ((1, 0),)), GriddedCayleyPerm(0, ((0, 0),))) at indices (0, 0) in direction 4 but only child and index 1 is non-empty, then Remove empty rows and columns
    +---+---+                   +---+---+                   +---+---+---+---+                       +---+---+---+---+       
    | 0 | 1 |                =  | 0 | 1 |                =  | 0 | # | # | 2 |                    =  | 0 | # | # | 2 |       
    +---+---+                   +---+---+                   +---+---+---+---+                       +---+---+---+---+       
    | # | # |                   Key:                        | # | ● | 1 | 1 |                       | # | ● | 1 | 1 |       
    +---+---+                   0: Av(01)                   +---+---+---+---+                       +---+---+---+---+       
    Key:                        1: Av(120,201,1010)         | # | # | # | # |                       Key:                    
    0: Av(01)                   Crossing obstructions:      +---+---+---+---+                       0: Av(01)               
    1: Av(120,201,1010)         10: ((0, 0),(1, 0))         Key:                                    1: Av(01,10)            
    Crossing obstructions:      Requirements 0:             0: Av(01)                               2: Av(120,201,1010)     
    10: ((0, 1),(1, 1))         0: ((0, 0))                 1: Av(01,10)                            Crossing obstructions:  
    Requirements 0:             Requirements 1:             2: Av(120,201,1010)                     01: ((1, 0),(2, 0))     
    0: ((0, 1))                 0: ((1, 0))                 Crossing obstructions:                  01: ((1, 0),(3, 0))     
    Requirements 1:                                         01: ((1, 1),(2, 1))                     01: ((2, 0),(3, 0))     
    0: ((1, 1))                                             01: ((1, 1),(3, 1))                     10: ((0, 1),(3, 0))     
                                                            01: ((2, 1),(3, 1))                     10: ((0, 1),(3, 1))     
                                                            10: ((0, 2),(3, 1))                     10: ((1, 0),(2, 0))     
                                                            10: ((0, 2),(3, 2))                     10: ((1, 0),(3, 0))     
                                                            10: ((1, 1),(2, 1))                     10: ((2, 0),(3, 0))     
                                                            10: ((1, 1),(3, 1))                     120: ((3, 1),(3, 1),(3, 0))
                                                            10: ((2, 1),(3, 1))                     201: ((3, 1),(3, 0),(3, 1))
                                                            120: ((3, 2),(3, 2),(3, 1))             1010: ((3, 1),(3, 0),(3, 1),(3, 0))
                                                            201: ((3, 2),(3, 1),(3, 2))             Requirements 0:         
                                                            1010: ((3, 2),(3, 1),(3, 2),(3, 1))     0: ((1, 0))             
                                                            Requirements 0:                         Requirements 1:         
                                                            0: ((1, 1))                             0: ((3, 0))             
                                                            Requirements 1:                         0: ((3, 1))             
                                                            0: ((3, 1))                                                     
                                                            0: ((3, 2))

    -------
    36 = 21
    Remove empty rows and columns
    +---+---+---+---+           +---+
    | # | # | # | # |        =  | ● |
    +---+---+---+---+           +---+
    | # | ● | # | # |           Key:
    +---+---+---+---+           Crossing obstructions:
    Key:                        Requirements 0:
    Crossing obstructions:      0: ((0, 0))
    Requirements 0:
    0: ((1, 0))

    -------
    37 = 23
    Remove empty rows and columns
    +---+---+---+---+           +---+
    | # | # | # | # |        =  | 0 |
    +---+---+---+---+           +---+
    | # | # | 0 | # |           Key:
    +---+---+---+---+           0: Av(01,10)
    Key:                        Crossing obstructions:
    0: Av(01,10)
    Crossing obstructions:

    -------
    38 = 39
    Remove empty rows and columns
    +---+---+---+---+                       +---+---+---+---+
    | 0 | 0 | # | 2 |                    =  | 0 | 0 | # | 2 |
    +---+---+---+---+                       +---+---+---+---+
    | # | # | # | # |                       | # | # | ● | 1 |
    +---+---+---+---+                       +---+---+---+---+
    | # | # | ● | 1 |                       Key:
    +---+---+---+---+                       0: Av(01)
    | # | # | # | # |                       1: Av(01,10)
    +---+---+---+---+                       2: Av(120,201,1010)
    Key:                                    Crossing obstructions:
    0: Av(01)                               00: ((0, 1),(1, 1))
    1: Av(01,10)                            01: ((0, 1),(1, 1))
    2: Av(120,201,1010)                     01: ((2, 0),(3, 0))
    Crossing obstructions:                  10: ((0, 1),(1, 1))
    00: ((0, 3),(1, 3))                     10: ((0, 1),(3, 1))
    01: ((0, 3),(1, 3))                     10: ((1, 1),(3, 1))
    01: ((2, 1),(3, 1))                     10: ((2, 0),(3, 0))
    10: ((0, 3),(1, 3))                     110: ((0, 1),(3, 1),(3, 0))
    10: ((0, 3),(3, 3))                     110: ((1, 1),(3, 1),(3, 0))
    10: ((1, 3),(3, 3))                     120: ((0, 1),(3, 1),(3, 0))
    10: ((2, 1),(3, 1))                     120: ((1, 1),(3, 1),(3, 0))
    110: ((0, 3),(3, 3),(3, 1))             120: ((3, 1),(3, 1),(3, 0))
    110: ((1, 3),(3, 3),(3, 1))             201: ((3, 1),(3, 0),(3, 1))
    120: ((0, 3),(3, 3),(3, 1))             1010: ((3, 1),(3, 0),(3, 1),(3, 0))
    120: ((1, 3),(3, 3),(3, 1))             Requirements 0:
    120: ((3, 3),(3, 3),(3, 1))             0: ((0, 1))
    201: ((3, 3),(3, 1),(3, 3))             Requirements 1:
    1010: ((3, 3),(3, 1),(3, 3),(3, 1))     0: ((2, 0))
    Requirements 0:
    0: ((0, 3))
    Requirements 1:
    0: ((2, 1))

    --------------
    39 -> (40, 41)
    Factor the tiling into factors
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    | 0 | 0 | # | 2 |                    =  | 0 | 0 | # | 2 |                    x  | # | # | # | # |
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    | # | # | ● | 1 |                       | # | # | # | 1 |                       | # | # | ● | # |
    +---+---+---+---+                       +---+---+---+---+                       +---+---+---+---+
    Key:                                    Key:                                    Key:
    0: Av(01)                               0: Av(01)                               Crossing obstructions:
    1: Av(01,10)                            1: Av(01,10)                            Requirements 0:
    2: Av(120,201,1010)                     2: Av(120,201,1010)                     0: ((2, 0))
    Crossing obstructions:                  Crossing obstructions:
    00: ((0, 1),(1, 1))                     00: ((0, 1),(1, 1))
    01: ((0, 1),(1, 1))                     01: ((0, 1),(1, 1))
    01: ((2, 0),(3, 0))                     10: ((0, 1),(1, 1))
    10: ((0, 1),(1, 1))                     10: ((0, 1),(3, 1))
    10: ((0, 1),(3, 1))                     10: ((1, 1),(3, 1))
    10: ((1, 1),(3, 1))                     110: ((0, 1),(3, 1),(3, 0))
    10: ((2, 0),(3, 0))                     110: ((1, 1),(3, 1),(3, 0))
    110: ((0, 1),(3, 1),(3, 0))             120: ((0, 1),(3, 1),(3, 0))
    110: ((1, 1),(3, 1),(3, 0))             120: ((1, 1),(3, 1),(3, 0))
    120: ((0, 1),(3, 1),(3, 0))             120: ((3, 1),(3, 1),(3, 0))
    120: ((1, 1),(3, 1),(3, 0))             201: ((3, 1),(3, 0),(3, 1))
    120: ((3, 1),(3, 1),(3, 0))             1010: ((3, 1),(3, 0),(3, 1),(3, 0))
    201: ((3, 1),(3, 0),(3, 1))             Requirements 0:
    1010: ((3, 1),(3, 0),(3, 1),(3, 0))     0: ((0, 1))
    Requirements 0:
    0: ((0, 1))
    Requirements 1:
    0: ((2, 0))

    -------
    40 = 14
    Remove empty rows and columns, then Either avoid or contain frozenset({GriddedCayleyPerm(0, ((1, 1),))}) but only child and index 0 is non-empty, then Remove empty rows and columns
    +---+---+---+---+                       +---+---+---+                           +---+---+---+                           +---+---+
    | 0 | 0 | # | 2 |                    =  | 0 | 0 | 2 |                        =  | 0 | # | 2 |                        =  | 0 | 2 |
    +---+---+---+---+                       +---+---+---+                           +---+---+---+                           +---+---+
    | # | # | # | 1 |                       | # | # | 1 |                           | # | # | 1 |                           | # | 1 |
    +---+---+---+---+                       +---+---+---+                           +---+---+---+                           +---+---+
    Key:                                    Key:                                    Key:                                    Key:
    0: Av(01)                               0: Av(01)                               0: Av(01)                               0: Av(01)
    1: Av(01,10)                            1: Av(01,10)                            1: Av(01,10)                            1: Av(01,10)
    2: Av(120,201,1010)                     2: Av(120,201,1010)                     2: Av(120,201,1010)                     2: Av(120,201,1010)
    Crossing obstructions:                  Crossing obstructions:                  Crossing obstructions:                  Crossing obstructions:
    00: ((0, 1),(1, 1))                     00: ((0, 1),(1, 1))                     10: ((0, 1),(2, 1))                     10: ((0, 1),(1, 1))
    01: ((0, 1),(1, 1))                     01: ((0, 1),(1, 1))                     110: ((0, 1),(2, 1),(2, 0))             110: ((0, 1),(1, 1),(1, 0))
    10: ((0, 1),(1, 1))                     10: ((0, 1),(1, 1))                     120: ((0, 1),(2, 1),(2, 0))             120: ((0, 1),(1, 1),(1, 0))
    10: ((0, 1),(3, 1))                     10: ((0, 1),(2, 1))                     120: ((2, 1),(2, 1),(2, 0))             120: ((1, 1),(1, 1),(1, 0))
    10: ((1, 1),(3, 1))                     10: ((1, 1),(2, 1))                     201: ((2, 1),(2, 0),(2, 1))             201: ((1, 1),(1, 0),(1, 1))
    110: ((0, 1),(3, 1),(3, 0))             110: ((0, 1),(2, 1),(2, 0))             1010: ((2, 1),(2, 0),(2, 1),(2, 0))     1010: ((1, 1),(1, 0),(1, 1),(1, 0))
    110: ((1, 1),(3, 1),(3, 0))             110: ((1, 1),(2, 1),(2, 0))             Requirements 0:                         Requirements 0:
    120: ((0, 1),(3, 1),(3, 0))             120: ((0, 1),(2, 1),(2, 0))             0: ((0, 1))                             0: ((0, 1))
    120: ((1, 1),(3, 1),(3, 0))             120: ((1, 1),(2, 1),(2, 0))                                                     
    120: ((3, 1),(3, 1),(3, 0))             120: ((2, 1),(2, 1),(2, 0))
    201: ((3, 1),(3, 0),(3, 1))             201: ((2, 1),(2, 0),(2, 1))
    1010: ((3, 1),(3, 0),(3, 1),(3, 0))     1010: ((2, 1),(2, 0),(2, 1),(2, 0))
    Requirements 0:                         Requirements 0:
    0: ((0, 1))                             0: ((0, 1))

    -------
    41 = 21
    Remove empty rows and columns
    +---+---+---+---+           +---+
    | # | # | # | # |        =  | ● |
    +---+---+---+---+           +---+
    | # | # | ● | # |           Key:
    +---+---+---+---+           Crossing obstructions:
    Key:                        Requirements 0:
    Crossing obstructions:      0: ((0, 0))
    Requirements 0:
    0: ((2, 0))

    --------
    42 -> ()
    is empty
    +---+---+---+---+
    | ∅ | ∅ | ∅ | ∅ |
    +---+---+---+---+
    | ∅ | ∅ | ∅ | ∅ |
    +---+---+---+---+
    | ∅ | ∅ | ∅ | ∅ |
    +---+---+---+---+
    | ∅ | ∅ | ∅ | ∅ |
    +---+---+---+---+
    Key:
    ∅: Av(ε)
    Crossing obstructions:
    Requirements 0:

        >>> spec.show()
    [I 250411 11:35:00 specification_drawer:543] Opening specification in browser
    [I 250411 11:35:04 specification_drawer:529] specification html file removed

Any method from ``CombinatorialSpecification`` can be used, but in particular the ``get_genf`` function finds the generating function and counts or the counts can be found using the specification as a recurrence up to length :math:`n` for any :math:`n`.

.. code-block:: python

        >>> spec.get_genf()
    [I 250411 11:36:55 specification:385] Computing initial conditions
    [I 250411 11:36:55 specification:359] Computing initial conditions
    [I 250411 11:36:55 specification:387] The system of 43 equations
        root_func := F_0:
        eqs := [
        F_0 = F_1 + F_3,
        F_1 = F_2,
        F_2 = 1,
        F_3 = F_4,
        F_4 = F_20*F_5,
        F_5 = F_6,
        F_6 = F_14 + F_7,
        F_7 = F_8,
        F_8 = F_10 + F_9,
        F_9 = F_2,
        F_10 = F_11 + F_12 + F_13,
        F_11 = 0,
        F_12 = F_4,
        F_13 = F_4,
        F_14 = F_15 + F_28,
        F_15 = F_16,
        F_16 = F_17,
        F_17 = F_18*F_20*F_22,
        F_18 = F_19,
        F_19 = F_1 + F_16,
        F_20 = F_21,
        F_21 = x,
        F_22 = F_23,
        F_23 = F_1 + F_24,
        F_24 = F_25,
        F_25 = F_26*F_27,
        F_26 = F_21,
        F_27 = F_23,
        F_28 = F_29 + F_30 + F_38 + F_42,
        F_29 = 0,
        F_30 = F_31,
        F_31 = F_32*F_36*F_37,
        F_32 = F_33,
        F_33 = F_34 + F_35,
        F_34 = F_10,
        F_35 = F_31,
        F_36 = F_21,
        F_37 = F_23,
        F_38 = F_39,
        F_39 = F_40*F_41,
        F_40 = F_14,
        F_41 = F_21,
        F_42 = 0
        ]:
        count := [1, 1, 3, 11, 41, 151, 553]:
    [I 250411 11:36:55 specification:388] Solving...
    [I 250411 11:36:58 specification:399] Checking initial conditions for: (2*x**3 - 4*x**2 + 4*x - 1)/(4*x**3 - 6*x**2 + 5*x - 1)
    >>> n = 10
    >>> print([spec.count_objects_of_size(i) for i in range(n)])
    [1, 1, 3, 11, 41, 151, 553, 2023, 7401, 27079]
