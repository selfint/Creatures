# neat_parameters.py
# Description: neat algorithm configurations.
# ---------------------------------------------------------------------------------------------------------------------

# Imports.
import math


# Activation function
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + pow(math.e, -4.9 * x))


# General
POPULATION_SIZE = 20
CREATURE_INPUTS = 2
CREATURE_OUTPUTS = 5

# Generation
GENERATION_TIME = 500
BOTTOM_PERCENT = 0.1
BIG_SPECIES = 5
NEW_CHILDREN = 1

# New Creature
CROSSOVER_RATE = 0.75
INTER_SPECIES_MATE = 0.001

# Dna
BASE_DNA = 'CONNECTED'

# Weights
WEIGHT_RANGE = 2.0
WEIGHT_MUTATION_RATE = 0.8
WEIGHT_PERTURB_RATE = 0.9
WEIGHT_PERTURB_AMOUNT = 0.1

# Bias
BIAS_RANGE = 2.0
BIAS_MUTATION_RATE = 0.8
BIAS_PERTURB_RATE = 0.9
BIAS_PERTURB_AMOUNT = 0.1

# Connection
CONNECTION_MUTATION_RATE = 0.05

# Node
NODE_MUTATION_RATE = 0.03

# Genetic Distance
EXCESS_CONSTANT = 1.0
DISJOINT_CONSTANT = 1.0
DELTA_WEIGHT_CONSTANT = 0.4
DISTANCE_THRESHOLD = 3

# Creature
CREATURE_HEALTH = 100
