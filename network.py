# network.py
# Description: network object for creature.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import Dict, Tuple, Union, Set, List

# Constants
from Constants.types import NodeObject
# Objects
from connection import Connection
from node import InputNode, OutputNode


class Network:

    def __init__(self, nodes: Dict[int, NodeObject],
                 node_connections: Dict[NodeObject, Dict[str, Tuple[Connection]]]):
        self.nodes = nodes
        self.node_connections = node_connections
        self.input_nodes = [node for node in self.nodes.values() if isinstance(node, InputNode)]
        self.output_nodes = [node for node in self.nodes.values() if isinstance(node, OutputNode)]

    def get_output(self, network_inputs: List[float]) -> List[float]:
        """
        Gets the output of the network. Evaluates a node's output recursively.
        :param network_inputs: A list of floats for the network.
        """
        for node in self.nodes.values():
            node.reset_node()

        for node, value in zip(self.input_nodes, network_inputs):
           node.set_input(value)
        return [self.get_node_output(node) for node in self.output_nodes]

    def get_node_output(self, node: NodeObject,
                        prev_connections: Set[int] = None) -> float:
        """
        Gets the recursive output of a node.
        :param node: Node to get output of.
        :param prev_connections: All connections that have been calculated to avoid infinite loops.
        :return: Node's output value.
        """

        # Get all nodes that add input into node.
        prev_connections = prev_connections or set()
        input_connections = self.node_connections[node]['dst']

        # Check for calculated connections.
        input_connections = [input_connection for input_connection in input_connections
                             if input_connection.number not in prev_connections]
        prev_connections.update(set(input_connection.number
                              for input_connection in input_connections))

        # Get each input nodes output and corresponding weight.
        inputs = [self.get_node_output(self.nodes[input_connection.src_number], prev_connections)
                  * input_connection.weight for input_connection in input_connections]

        # Set node input
        node.set_input(inputs)
        output = node.get_output()

        return output

    def get_node_connection(self, src: int, dst: int) -> Union[Connection, None]:
        """
        Finds a old_connection between two nodes, returns None if there isn't one.
        """
        out_connections = self.node_connections[self.nodes[src]]['dst']

        # Get all connections outputting from the source node,
        # and check if they output to the destination node,
        for conn in out_connections:
            if conn.dst_number == dst:
                return conn
        return None


if __name__ == '__main__':
    pass
