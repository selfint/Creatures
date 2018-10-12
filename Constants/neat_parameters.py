# neat_parameters.py
# Description: neat algorithm configurations.
# ---------------------------------------------------------------------------------------------------------------------

# Imports.
import math


# Activation function
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + pow(math.e, -4.9 * x))


# General
POPULATION_SIZE = 2
CREATURE_INPUTS = 2
CREATURE_OUTPUTS = 5

# Dna
BASE_DNA = 'CONNECTED'

# Weights
WEIGHT_RANGE = 2.0
WEIGHT_MUTATION_RATE = 1
WEIGHT_PERTURB_RATE = 0.1
WEIGHT_PERTURB_AMOUNT = 0.1

# Bias
BIAS_RANGE = 2.0
BIAS_MUTATION_RATE = 1
BIAS_PERTURB_RATE = 0.2
BIAS_PERTURB_AMOUNT = 0.1

# Connection
CONNECTION_MUTATION_RATE = 1

# Node
NODE_MUTATION_RATE = 1

# Genetic Distance
EXCESS_CONSTANT = 1.0
DISJOINT_CONSTANT = 1.0
DELTA_WEIGHT_CONSTANT = 0.4
DISTANCE_THRESHOLD = 3.0
