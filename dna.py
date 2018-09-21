# dna.py
# Description: dna object for creature.
# ---------------------------------------------------------------------------------------

# Imports
from typing import Dict, Tuple, Union

from connection import Connection
from functions import dict_string
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

	def __init__(self, inputs: int, outputs: int, weight_range: float, nodes: Dict[
		int, Union[InputNode, HiddenNode, OutputNode]] = None, connections: Dict[int, Connection] = None):
		self.inputs = inputs
		self.outputs = outputs
		self.weight_range = self.bias_range = weight_range

		# Generate nodes if not given any.
		self.nodes = nodes if nodes is not None else self.generate_nodes()
		self.input_nodes = self.get_node_by_type(InputNode)
		self.output_nodes = self.get_node_by_type(OutputNode)

		# Generate connections if not given any.
		self.connections = connections if connections is not None else self.connect_nodes()
		self.node_connections = {node: self.get_node_connections(node) for node in self.nodes.values()}

	def __str__(self):
		return FULL_STRING.format(self.input_nodes, self.get_node_by_type(HiddenNode), self.output_nodes,
								  dict_string(self.node_connections))

	def __repr__(self):
		return str(self)

	def generate_nodes(self) -> Dict[int, Union[InputNode, HiddenNode, OutputNode]]:
		"""
		Generates input and output nodes.
		"""

		nodes = []
		for n in range(self.inputs):
			nodes.append(InputNode(len(nodes)))
		for n in range(self.outputs):
			nodes.append(OutputNode(len(nodes), self.bias_range))

		return {node.number: node for node in nodes}

	def get_node_by_type(self, node_type: type) -> Tuple[Union[InputNode, HiddenNode, OutputNode]]:
		"""
		Finds all nodes of type node_type.
		"""
		return tuple(node for node in self.nodes.values() if type(node) is node_type)

	def connect_nodes(self) -> Dict[int, Connection]:
		"""
		Fully connects all input nodes to output nodes.
		:return: Dict of indexes corresponding with connections.
		"""

		connections = []
		for src in self.input_nodes:
			for dst in self.output_nodes:
				connections.append(Connection(len(connections), src.number, dst.number, self.weight_range))

		return {connection.number: connection for connection in connections}

	def get_node_connections(self, node: Union[InputNode, HiddenNode, OutputNode]) \
			-> Dict[str, Tuple[Connection]]:
		"""
		Returns all connections from node and into node (src, dst).
		:param node: Node object.
		"""
		src = tuple(connection for connection in self.connections.values() if connection.src_number == node.number)
		dst = tuple(connection for connection in self.connections.values() if connection.dst_number == node.number)

		return {'src': src, 'dst': dst}


if __name__ == '__main__':
	n = Dna(2, 1, 2)
	print(n)


