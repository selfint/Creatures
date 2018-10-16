# main.py
# Description: project constants.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import sys

# Constants
from Constants.constants import CAPTION, HEIGHT, WIDTH
# Objects
from graphics import Graphics
from simulation import Simulation

# Run simulation.
if __name__ == '__main__':
    simulation = Simulation()
    graphics = Graphics(simulation, WIDTH, HEIGHT, CAPTION)
    graphics.run()
    sys.exit(1)










