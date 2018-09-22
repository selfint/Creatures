# main.py
# Description: main.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from graphics import Graphics
from simulation import Simulation

# Constants

if __name__ == '__main__':
    s = Simulation(1, 2, 1)
    g = Graphics(s)
    g.run()