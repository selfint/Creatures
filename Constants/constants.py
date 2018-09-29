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

# Amount of "#" meaning: 1 -> Node number, 2 -> Connection number, 3 -> Mutation number.
CONNECTION_STRING = "<Connection ##{}({}): #{} -({:.2f})-> #{}>"
NODE_STRING = "<{} #{} bias: {:.3f}>"
BASE_MUTATION_STRING = "<{} :: {}"
NUMBERED_MUTATION_STRING = "<{} ###{}:: {}>"
WEIGHT_MUTATION_STRING = "<Connection ##{}: #{} -({:.2f} => {:.2f})-> #{}>"
BIAS_MUTATION_STRING = "<{} #{} bias: {:.3f} => {:.3f}>"
NODE_MUTATION_STRING = "< Split: {} | Src: {} | Node: {} | dst: {} >"
CREATURE_STRING = ""

# Graphics.
CAPTION = 'Creatures'
WIDTH, HEIGHT = 800, 600
SPEED_SCALING = 0.1
CREATURE_COLORS = {  # Will be used to visually differentiate between species.
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

