# data_structures.py
# Description: data structures.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from collections import namedtuple


# Data structures.
# - Creature -
# Creature information is mutable, so cant use named tuple
class CreatureInfo:

    def __init__(self, x: float, y: float, scale: float):
        self.x = x
        self.y = y
        self.scale = scale

CreatureNetworkInput = namedtuple('NetworkInput', 'dx dy')
CreatureNetworkOutput = namedtuple('NetworkOutput', 'left right up down urgency')
# Each variable that has a matching name in CreatureInfo shows how to change that variable.
# For example: CreatureInfo(x=100, y=100, scale=1) + CreatureActions(x=1, y=-0.3) = CreatureInfo(x=101, y=99.7, scale=1)
CreatureActions = namedtuple('CreatureActions', 'x y')
