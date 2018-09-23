# types.py
# Description: types.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import Union, Tuple

from node import InputNode, HiddenNode, OutputNode

# Type abbreviations.
NodeObject = Union[InputNode, HiddenNode, OutputNode]
COLOR = Tuple[float, float, float]
