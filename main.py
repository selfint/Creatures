# main.py
# Description: project constants.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import sys

from Constants.constants import TEXT_ONLY
from graphics import Graphics
from simulation import Simulation

# Run simulation.
if __name__ == '__main__':
    print("Starting simulation.")
    simulation = Simulation()
    graphics = Graphics(simulation)

    mode = 2  # input('Which mode to run (1-graphical, 2-textual) ')
    if TEXT_ONLY:
        graphics.text_run()
    else:
        graphics.graphical_run()
    sys.exit(1)





