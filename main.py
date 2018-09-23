# main.py
# Description: main.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from graphics import Graphics
from simulation import Simulation

# Constants
from constants import CAPTION, CREATURE_INPUTS, CREATURE_OUTPUTS, HEIGHT, POPULATION_SIZE, WIDTH


if __name__ == '__main__':
    simulation = Simulation(POPULATION_SIZE, CREATURE_INPUTS, CREATURE_OUTPUTS)
    creature1, creature2 = simulation.population.keys()
    c1, c2 = simulation.population.values()
    temp1 = simulation.info_to_vec(c1, c2)
    temp2 = simulation.info_to_vec(c2, c1)
    graphics = Graphics(simulation, WIDTH, HEIGHT, CAPTION)
    graphics.run()