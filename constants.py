# constants.py
# Description: type objects for projects.
# ---------------------------------------------------------------------------------------------------------------------
import collections
from typing import Union, Tuple

from node import InputNode, HiddenNode, OutputNode

Node = Union[InputNode,HiddenNode,OutputNode]
COLOR = Tuple[float, float, float]
CreatureInfo = collections.namedtuple('CreatureInfo', 'x y scale')

CREATURE_COLORS = {
'RED' : (255, 0, 0),
'GREEN' : (0, 255, 0),
'BLUE' : (0, 0, 255),
'PINK': (255, 0, 255)
}
