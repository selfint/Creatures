# main.py
# Description: project constants.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import sys

from graphics import Graphics
from simulation import Simulation

# Run simulation.
if __name__ == '__main__':
    print("Starting simulation.")
    simulation = Simulation()
    graphics = Graphics(simulation)
    graphics.run()
    sys.exit(1)





