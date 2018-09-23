# main.py
# Description: project constants.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import sys

# Constants
from Constants.constants import WIDTH, HEIGHT, CAPTION
from Constants.neat_parameters import POPULATION_SIZE, CREATURE_INPUTS, CREATURE_OUTPUTS
# Objects
from graphics import Graphics
from simulation import Simulation

# Run simulation.
if __name__ == '__main__':
    simulation = Simulation(POPULATION_SIZE, CREATURE_INPUTS, CREATURE_OUTPUTS)
    graphics = Graphics(simulation, WIDTH, HEIGHT, CAPTION)
    graphics.run()
    sys.exit(1)










