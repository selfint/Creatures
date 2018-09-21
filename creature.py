# creature.py
# Description: creature object.
# ---------------------------------------------------------------------------------------

# Imports
from network import Network
from dna import Dna


# Constants
WEIGHT_RANGE = 2.0

class Creature:

	def __init__(self, inputs: int, outputs: int, name='Creature', weight_range=WEIGHT_RANGE):
		self.inputs = inputs
		self.outputs = outputs
		self.name = name

		self.weight_range = weight_range

		self.dna = Dna(self.inputs, self.outputs, self.weight_range)
		self.network = Network(self.dna.nodes, self.dna.node_connections)



if __name__ == '__main__':
	c = Creature(20, 3)
	print(c.network.get_output([1 for _ in range(c.inputs)]))
	print(c.network.get_output([0 for _ in range(c.inputs)]))
