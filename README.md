# CayleyPermutationsInsEnc
This is a python library for enumerating Cayley permutations with the insertion encoding.

### Installing

### Cayley Permutations
A Cayley permutation is a word $\pi \in \mathbb{N}^*$ such that every number between 1 and the maximum value of $\pi$ appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. 

There are two types of insertion encoding for enumerating Cayley permutations. The vertical insertion encoding inserts new maxima in the Cayley permutation and horizontal insertion encoding inserts new rightmost values.
 
For more information, please see...


### Creating a Cayley permutation
The input to a Cayley permutation can be one-based or zero-based and will adjust to being zero-based automatically, but it must be a valid Cayley permutation.

For example:
`<CayleyPermutation((0,0,0))>`
`<CayleyPermutation([1,1,1])>`
`<CayleyPermutation((2,2,2))>`