# my_types.py
# Description: type objects for projects.
# ---------------------------------------------------------------------------------------------------------------------
import collections
from typing import Union, Tuple

from node import InputNode, HiddenNode, OutputNode

Node = Union[InputNode,HiddenNode,OutputNode]
COLOR = Tuple[float, float, float]
GraphicInfo = collections.namedtuple('GraphicInfo', 'x y scale')
CreatureInfo = collections.namedtuple('CreatureInfo', 'x y scale')

