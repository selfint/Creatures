# network.py
# Description: network object for creature.
# ---------------------------------------------------------------------------------------

# Imports
from typing import Dict, Tuple, Union

from connection import Connection
from node import *

# Constants


class Network:

	def __init__(self, nodes: Dict[int, Union[InputNode, HiddenNode, OutputNode]],
				 node_connections: Dict[Union[InputNode, HiddenNode, OutputNode], Dict[str, Tuple[Connection]]]):
		self.nodes = nodes
		self.node_connections = node_connections
		self.inputs = [node for node in self.nodes.values() if type(node) is InputNode]
		self.outputs = [node for node in self.nodes.values() if type(node) is OutputNode]

	def get_output(self, inputs: List[float]) -> List[float]:
		"""
		Gets the output of the network. Evaluates a node's output recursively.
		:param inputs: A list of floats for the network.
		:return: A list of floats.
		"""
		for node in self.nodes.values():
			node.reset_node()

		for i in range(len(inputs)):
			self.inputs[i].set_input(inputs[i])
		return [self.get_node_output(node) for node in self.outputs]

	def get_node_output(self, node: Union[InputNode, HiddenNode, OutputNode]) -> float:
		"""
		Gets the recursive output of a node.
		:param node: Node to get output of.
		:return: Node's output value.
		"""

		# Get all nodes that add input into node.
		input_connections = self.node_connections[node]['dst']
		input_nodes = [self.nodes[input_connection.src_number] for input_connection in input_connections]

		# Get all input node outputs
		inputs = [self.get_node_output(input_node) for input_node in input_nodes]

		# Set node input
		node.set_input(inputs)
		output = node.get_output()

		return output


if __name__ == '__main__':
	pass
