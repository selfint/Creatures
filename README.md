# Creatures
Evolving creatures using NEAT algorithm, based on this paper: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

## In a nutshell
The ultimate goal of this project is to learn how to use the NEAT algorithm, as explained in the paper linked above. The
simulation will contain creatures that can represent a dna. It will let each creature act, basing its actions 
(receiving its inputs) on all other creatures in its line-of-sight. In essence, by SEEING the creatures and learning to
analyze them.

Because of the speciation functionality of NEAT, I would like to see separate species evolve, and stick together. 
The basic options that each creature will be able to do is MOVE, ATTACK, MATE, EAT (not 100% but that is the goal at 
this point). To encourage separate species to stick together, a new child will be born next to one or both of the parents.
Attacking will not be rewarded, but it will not be penalized either, it is an option that is possible and should be used
only if it benefits the creature. The overall fitness of a creature is relative to its species, per the paper, and by how
many kids it created.

## Hopes
If the creatures divide into tribes on their own, that will be nice.
If the creatures attack as a group that would be amazing, but this is unlikely.
Seeing if adding one or two output node, that will be "seen" by each creature receiving this creature as input will lead to
some sort of benefit in the species' success. This is very unlikely but interesting nonetheless.
