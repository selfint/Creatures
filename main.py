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

if __name__ == '__main__':
    s = Simulation(1, 2, 1)
    g = Graphics(s, width=WIDTH, height=HEIGHT, caption=CAPTION)
    g.run()