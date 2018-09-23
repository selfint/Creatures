# constants.py
# Description: type objects for projects.
# ---------------------------------------------------------------------------------------------------------------------
import collections
from typing import Union, Tuple

from node import InputNode, HiddenNode, OutputNode

WIDTH, HEIGHT = 800, 600
CAPTION = 'Creatures'
POPULATION_SIZE = 2
CREATURE_INPUTS = 2
CREATURE_OUTPUTS = 4

Node = Union[InputNode,HiddenNode,OutputNode]
COLOR = Tuple[float, float, float]
CreatureInfo = collections.namedtuple('CreatureInfo', 'x y scale')

# Network input to make decision for a CREATURE (for other object another network is needed).
CreatureNetworkInput = collections.namedtuple('NetworkInput', 'dx dy')

CREATURE_COLORS = {
'RED' : (255, 0, 0),
'GREEN' : (0, 255, 0),
'BLUE' : (0, 0, 255),
'PINK': (255, 0, 255),
'CYAN': (0, 255, 255)
}
