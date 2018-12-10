# main.py
# Description: project constants.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import sys

from graphics import Graphics
from simulation import Simulation

# Run simulation.
if __name__ == '__main__':
    simulation = Simulation()
    graphics = Graphics(simulation)

    mode = input('Which mode to run (1-graphical, 2-textual) ')
    if mode == '1':
        graphics.graphical_run()
    elif mode == '2':
        graphics.text_run()
    else:
        raise ValueError(mode, "is not acceptable.")
    sys.exit(1)





