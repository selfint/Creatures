# network.py
# Description: network object for creature.
# ---------------------------------------------------------------------------------------

# Imports
from typing import Tuple, List
from connection import Connection
from node import BaseNode


class Network:

	def __init__(self, inputs: int, outputs: int, weight_range: int, nodes: Tuple[BaseNode] = tuple(),
				 connections: Tuple[Connection] = tuple()):
		self.inputs = inputs
		self.outputs = outputs
		self.weight_range = weight_range
		self.nodes = nodes
		self.connections = connections if connections else self.connect_nodes()
		self.node_connections = {node: self.get_node_connections(node) for node in nodes}

	def get_node_connections(self, node: BaseNode) -> Tuple[List[Connection], List[Connection]]:
		"""
		Returns all connections from node and into node.
		:param node: Node object.
		:return: Src connections (connections where node is src), Dst connections (connections where node is dst).
		"""
		src = [connection for connection in self.connections if connection.src_number == node.number]
		dst = [connection for connection in self.connections if connection.dst_number == node.number]
		return src, dst

	def connect_nodes(self) -> None:
		"""
		Fully connects all input nodes to output nodes.
		"""


if __name__ == '__main__':
	n = Network(2, 1, 2)
