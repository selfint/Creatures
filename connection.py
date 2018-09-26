# old_connection.py
# Description: old_connection object for network.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import random
from typing import Union

from Constants.constants import CONNECTION_STRING
from Constants.neat_parameters import WEIGHT_RANGE


class Connection:

    def __init__(self, number: Union[int, None], src_number: Union[int, None], dst_number: Union[int, None],
                 weight_range: float = WEIGHT_RANGE, weight: float = None, enabled: bool = True):
        self.number = number
        self.src_number = src_number
        self.dst_number = dst_number
        self.weight_range = weight_range

        # Calculate random weight_value
        self.weight = weight if weight else random.random() * weight_range * 2 - weight_range
        self.enabled = enabled

    def __str__(self):
        return CONNECTION_STRING.format(self.number, '+' if self.enabled else '-',
                                        self.src_number, self.weight, self.dst_number)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    c = Connection(0, 1, 2, True)
    print(c)
