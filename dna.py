# dna.py
# Description: dna object for creature.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import Dict, Tuple, Type, List

# Constants
from Constants.constants import DNA_STRING
from Constants.neat_parameters import BIAS_RANGE
from Constants.types import NodeObject
# Objects
from connection import Connection
from functions import dict_string
from mutations import WeightMutation, BiasMutation, ConnectionMutation, NodeMutation, MutationObject
from node import InputNode, HiddenNode, OutputNode


class Dna:

    def __init__(self, inputs: int = None, outputs: int = None, nodes: Dict[int, NodeObject] = None,
                 connections: Dict[int, Connection] = None):

        # Take input & output node amount if given, else take values.
        self.inputs = len([node for node in nodes if isinstance(node, InputNode)]) \
            if nodes else inputs
        self.outputs = len([node for node in nodes if isinstance(node, OutputNode)]) \
            if nodes else outputs

        # Generate nodes if not given any.
        self.nodes = nodes or self.generate_nodes()
        self.input_nodes = self.get_node_by_type(InputNode)
        self.hidden = 0
        self.output_nodes = self.get_node_by_type(OutputNode)

        # Generate connections if not given any.
        self.connections = connections or self.connect_nodes()
        self.update_connections()

    def update_connections(self) -> None:
        """
        Generates main__a dictionary mapping nodes to all their connections.
        """
        self.node_connections = {node: self.get_node_connections(node) for node in self.nodes.values()}

    def __str__(self):
        return DNA_STRING.format(len(self.input_nodes), len(self.get_node_by_type(HiddenNode)), len(self.output_nodes),
                                  dict_string(self.node_connections))

    def __repr__(self):
        return str(self)

    def available_connections(self, shallow: bool = False) -> List[Tuple[int, int]]:
        """
        Returns all nodes that can be connected.
        :param shallow: If set, function will return the first available connection.
        """

        # Get all available connections by the following conditions:
        # 1. No duplicate connections.
        # 2. A connection cannot output into an InputNode.
        # 3. An OutputNode cannot output into an OutputNode, but main__a HiddenNode can output into main__a HiddenNode.
        available_connections = []
        connections = [(connection.src_number, connection.dst_number) for connection in self.connections.values()]
        for src_number in self.nodes:
            for dst_number in [node_number for node_number in self.nodes if node_number != src_number]:
                if (src_number, dst_number) not in connections:
                    dst_type = type(self.nodes[dst_number])
                    if dst_type is not InputNode:
                        src_type = type(self.nodes[src_number])
                        if src_type is not dst_type or src_type is HiddenNode:
                            available_connections.append((src_number, dst_number))
                            if shallow:
                                return available_connections

        return available_connections

    def generate_nodes(self) -> Dict[int, NodeObject]:
        """
        Generates input and output nodes.
        """

        nodes = []
        for n in range(self.inputs):
            nodes.append(InputNode(len(nodes)))
        for n in range(self.outputs):
            nodes.append(OutputNode(len(nodes), BIAS_RANGE))

        return {node.number: node for node in nodes}

    def get_node_by_type(self, node_type: Type[NodeObject]) -> Tuple[NodeObject]:
        """
        Finds all nodes of type node_type.
        """

        # Use type(x) is y, since we want exact types, ignoring inheritance.
        return tuple(node for node in self.nodes.values() if type(node) is node_type)

    def connect_nodes(self) -> Dict[int, Connection]:
        """
        Fully connects all input nodes to output nodes.
        :return: Dict of indexes corresponding with connections.
        """

        connections = []
        for src in self.input_nodes:
            for dst in self.output_nodes:
                # TODO 10/11/18 connect_nodes: Initially give connections NONE as number, maybe generate mutations?.
                connections.append(Connection(len(connections), src.number, dst.number))

        return {connection.number: connection for connection in connections}

    def get_node_connections(self, node: NodeObject) -> Dict[str, Tuple[Connection]]:
        """
        Returns all connections from node and into node (src, dst).
        :param node: Node object.
        """
        src = tuple(connection for connection in self.connections.values() if connection.src_number == node.number)
        dst = tuple(connection for connection in self.connections.values() if connection.dst_number == node.number)

        return {'src': src, 'dst': dst}

    def update(self, mutations: List[MutationObject]) -> None:
        """
        Applies all mutations, assumes all mutations have been configured.
        """
        for mutation in mutations:

            if type(mutation) is WeightMutation:
                mutation.connection.weight = mutation.new_weight

            elif type(mutation) is BiasMutation:
                mutation.node.bias = mutation.new_bias

            elif type(mutation) is ConnectionMutation:
                new_connection = mutation.connection
                self.connections[new_connection.number] = new_connection

            elif type(mutation) is NodeMutation:
                split_connection = mutation.old_connection
                split_connection.enabled = False

                self.nodes[mutation.new_node.number] = mutation.new_node
                self.connections[mutation.new_dst_connection.number] = mutation.new_dst_connection
                self.connections[mutation.new_src_connection.number] = mutation.new_src_connection

        # Re-map all nodes and connections.
        self.update_connections()
        self.hidden = len(self.get_node_by_type(HiddenNode))


if __name__ == '__main__':
    n = Dna(2, 1)
    print(n)
    print(n.get_node_by_type(OutputNode))
