# connection.py
# Description: connection object for network.
# ---------------------------------------------------------------------------------------

# Imports
import random
from typing import Union


class Connection:

	def __init__(self, src_number: int, dst_number: int, weight_range: float, forward: bool = True,
				 weight: Union[float, None] = None):
		self.src_number = src_number
		self.dst_number = dst_number
		self.weight_range = weight_range
		self.forward = forward

		# Calculate random weight_value
		self.weight = weight if weight else random.random() * weight_range * 2 - weight_range

if __name__ == '__main__':
	c = Connection(0, 1, 2, True)
