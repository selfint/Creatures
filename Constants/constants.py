# constants.py
# Description: constants.
# ---------------------------------------------------------------------------------------------------------------------

# Object strings.
DNA_STRING = """
Dna
Input  Nodes: {}
Hidden Nodes: {}
Output Nodes: {}

---  Connections ---
{}
--------------------
"""
CONNECTION_STRING = "Connection {}: {} -({:.2f})-> {}"
NODE_STRING = "{} {} bias: {:.3f}"

# Graphics.
CAPTION = 'Creatures'
WIDTH, HEIGHT = 800, 600
SPEED_SCALING = 0.01
CREATURE_COLORS = {  # Will be used to differentiate between species.
    'RED' : (255, 0, 0),
    'GREEN' : (0, 255, 0),
    'BLUE' : (0, 0, 255),
    'PINK': (255, 0, 255),
    'CYAN': (0, 255, 255)
}
BLACK = 0, 0, 0
GREY = 125, 125, 125
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
BACKGROUND = 230, 220, 50
CENTER = 0

