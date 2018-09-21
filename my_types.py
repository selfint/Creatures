# my_types.py
# Description: type objects for projects.
# ---------------------------------------------------------------------------------------
from typing import Union

from node import InputNode, HiddenNode, OutputNode

Node = Union[InputNode,HiddenNode,OutputNode]
