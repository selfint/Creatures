# data_structures.py
# Description: data structures.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from collections import namedtuple


# Data structures.
# - Creature -
# CreatureInfo = namedtuple('CreatureInfo', 'x y scale')
# Creature information is mutable, so cant use named tuple
class CreatureInfo:

    def __init__(self, x: float, y: float, scale: float):
        self.x = x
        self.y = y
        self.scale = scale
CreatureNetworkInput = namedtuple('NetworkInput', 'dx dy')
CreatureNetworkOutput = namedtuple('NetworkOutput', 'left right up down urgent')
CreatureActions = namedtuple('CreatureActions', 'move_x move_y')
