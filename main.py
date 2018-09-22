# main.py
# Description: main.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from graphics import Graphics
from simulation import Simulation

# Constants
HEIGHT = 600
WIDTH = 800
CAPTION = 'Creatures'
POPULATION_SIZE = 2
CREATURE_INPUTS = 2
CREATURE_OUTPUTS = 4


if __name__ == '__main__':
    simulation = Simulation(POPULATION_SIZE, CREATURE_INPUTS, CREATURE_OUTPUTS)
    graphics = Graphics(simulation, WIDTH, HEIGHT, CAPTION)
    graphics.run()