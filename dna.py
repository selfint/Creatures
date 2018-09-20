# dna.py
# Description: dna object for creature.
# ---------------------------------------------------------------------------------------

# Imports
from typing import Tuple, List, Union
from connection import Connection
from node import *

# Constants
FULL_STRING = """
Dna
--- Input  Nodes ---
{}

--- Hidden Nodes ---
{}

--- Output Nodes ---
{}

---  Connections ---
{}
"""


class Dna:

	def __init__(self, inputs: int, outputs: int, weight_range: int, nodes: Tuple[
		Union[InputNode, HiddenNode, OutputNode]] = tuple(),
				 connections: Tuple[Connection] = tuple()):
		self.inputs = inputs
		self.outputs = outputs
		self.weight_range = weight_range
		self.nodes = nodes if nodes else self.generate_nodes()
		self.input_nodes = self.get_node_by_type(InputNode)
		self.output_nodes = self.get_node_by_type(OutputNode)
		self.connections = connections if connections else self.connect_nodes()
		self.node_connections = {node: self.get_node_connections(node) for node in nodes}

	def __str__(self):
		return FULL_STRING.format(self.input_nodes, self.get_node_by_type(HiddenNode), self.output_nodes,
								  self.node_connections)

	def generate_nodes(self) -> Tuple[Union[InputNode, OutputNode]]:
		"""
		Generates input and output nodes.
		"""

		nodes = []
		for n in range(self.inputs):
			nodes.append(InputNode(len(nodes)))
		for n in range(self.outputs):
			nodes.append(OutputNode(len(nodes), self.weight_range))

		return tuple(nodes)

	def get_node_by_type(self, node_type: type) -> Tuple[Union[InputNode, HiddenNode, OutputNode]]:
		"""
		Finds all nodes of type node_type.
		"""
		return tuple(node for node in self.nodes if type(node) is node_type)

	def connect_nodes(self) -> Tuple[Connection]:
		"""
		Fully connects all input nodes to output nodes.
		"""

		connections = []
		for src in self.input_nodes:
			for dst in self.output_nodes:
				connections.append(Connection(len(connections), src.number, dst.number, self.weight_range))
		print(connections)
		return tuple(connections)

	def get_node_connections(self, node: Union[InputNode, HiddenNode, OutputNode]) \
			-> Tuple[List[Connection], List[Connection]]:
		"""
		Returns all connections from node and into node (src, dst).
		:param node: Node object.
		"""
		src = [connection for connection in self.connections if connection.src_number == node.number]
		dst = [connection for connection in self.connections if connection.dst_number == node.number]
		return src, dst


if __name__ == '__main__':
	n = Dna(2, 1, 2)
	print(n)


