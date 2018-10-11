# mutations.py
# Description: All possible mutation types.
# ---------------------------------------------------------------------------------------

# Imports
from abc import ABC, abstractmethod
from random import random
from typing import Union, List

# Constants
from Constants.constants import NUMBERED_MUTATION_STRING, WEIGHT_MUTATION_STRING, BIAS_MUTATION_STRING, \
    NODE_MUTATION_STRING, BASE_MUTATION_STRING
from Constants.neat_parameters import WEIGHT_RANGE, BIAS_RANGE, WEIGHT_PERTRUB_RATE, WEIGHT_PERTRUB_AMOUNT, \
    BIAS_PERTRUB_RATE, BIAS_PERTRUB_AMOUNT
from Constants.types import NodeObject
from connection import Connection
from node import HiddenNode


class Mutation(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        self.string = ''

    def __str__(self):
        return BASE_MUTATION_STRING.format(self.name, self.string)

    def __repr__(self):
        return str(self)


class Innovation(ABC):

    def __init__(self):
        super(Innovation, self).__init__()
        self.number = None
        self.name = self.__class__.__name__
        self.string = ''

    def __str__(self):
        return NUMBERED_MUTATION_STRING.format(self.name, self.number, self.string)

    def __repr__(self):
        return str(self)

    @abstractmethod
    def set_string(self) -> None:
        """
        Builds the string that represents the mutation.
        """

    @abstractmethod
    def configure(self, *args) -> None:
        """
        Sets the numbers for dst connection, new node and src connection.
        """

    @abstractmethod
    def calc_configurations(self, connection_count: int, node_count: int) -> List[int]:
        """
        Receives connection count and node count
        """

    @abstractmethod
    def unique(self) -> list:
        """
        Returns identifying information, not including mutation number.
        """

    @abstractmethod
    def configurations(self) -> tuple:
        """
        Returns all values that configure the mutation.
        """


class WeightMutation(Mutation):

    def __init__(self, connection: Connection):
        super(WeightMutation, self).__init__()
        self.connection = connection

        # Number of the CONNECTION this mutation updates, not the number of the mutation itself.
        self.number = connection.number
        number, src, weight, dst = connection.number, connection.src_number, connection.weight, connection.dst_number

        # Randomly choose between perturbing the weight or completely changing it.
        if random() < WEIGHT_PERTRUB_RATE:
            self.new_weight = weight + (random() * 2 - 1) * WEIGHT_PERTRUB_AMOUNT
        else:
            self.new_weight = random() * WEIGHT_RANGE * 2 - WEIGHT_RANGE

        # Generate mutation string.
        self.string = WEIGHT_MUTATION_STRING.format(number, src, weight, self.new_weight, dst)


class BiasMutation(Mutation):

    def __init__(self, node: NodeObject):
        super(BiasMutation, self).__init__()
        self.node = node
        name, number, bias = node.name, node.number, node.bias

        # Number of the NODE this mutation updates, not the number of the mutation itself.
        self.number = node.number

        # Randomly choose between perturbing the bias or completely changing it.
        if random() < BIAS_PERTRUB_RATE:
            self.new_bias = self.node.bias + (random() * 2 - 1) * BIAS_PERTRUB_AMOUNT
        else:
            self.new_bias = random() * BIAS_RANGE * 2 - BIAS_RANGE

        # Generate mutation string.
        self.string = BIAS_MUTATION_STRING.format(name, number, bias, self.new_bias)


class ConnectionMutation(Innovation):

    def __init__(self, number: Union[int, None] = None, src_number: Union[int, None] = None,
                 dst_number: Union[int, None] = None, connection: Union[Connection, None] = None):
        super(ConnectionMutation, self).__init__()

        # Number can be None, but src and dst must be a number.
        self.number = number if not connection else connection.number
        self.src_number = src_number if not connection else connection.src_number
        self.dst_number = dst_number if not connection else connection.dst_number
        self.connection = connection or Connection(None, self.src_number, self.dst_number)
        self.set_string()

    def set_string(self) -> None:
        self.string = str(self.connection)

    def configure(self, number: int) -> None:
        self.number = number or self.number
        self.connection.number = number or self.number
        self.set_string()

    def calc_configurations(self, connection_count:int, node_count: int):
        self.configure(connection_count + 1)
        return connection_count + 1, node_count

    def unique(self):
        return self.src_number, self.dst_number

    def configurations(self):
        return self.number,


class NodeMutation(Innovation):

    def __init__(self, connection: Connection):
        super(NodeMutation, self).__init__()
        self.number = connection.number
        self.old_connection = connection

        # Disable connection that is being split.
        old_src, old_dst, old_weight = connection.src_number, connection.dst_number, connection.weight

        # The number of the connection this node split, will be used to identify identical node mutations.
        self.connection_number = connection.number

        # src----old_connection--->dst
        # src-dst_conn->new_node->src_conn->dst
        # Connection that has new_node as DST.
        self.new_node = HiddenNode(None, BIAS_RANGE)
        self.new_dst_connection = Connection(None, old_src, self.new_node.number, 1)

        # Connection that has new_node as SRC.
        self.new_src_connection = Connection(None, self.new_node.number, old_dst, old_weight)
        self.set_string()

    def set_string(self) -> None:
        self.string = NODE_MUTATION_STRING.format(self.old_connection, self.new_dst_connection, self.new_node,
                                                  self.new_src_connection)

    def configure(self, dst_connection_number: int, new_node_number: int, src_connection_number: int) -> None:
        """
        Sets the numbers for dst connection, new node and src connection.
        """
        self.new_dst_connection.number = dst_connection_number
        self.new_dst_connection.dst_number = new_node_number
        self.new_node.number = new_node_number
        self.new_src_connection.src_number = new_node_number
        self.new_src_connection.number = src_connection_number
        self.set_string()

    def calc_configurations(self, connection_count: int, node_count: int):
        self.configure(connection_count + 1, node_count + 1, connection_count + 2)
        return connection_count + 2, node_count + 1

    def unique(self):
        return self.connection_number

    def configurations(self):
        return self.new_dst_connection.number, self.new_node.number, self.new_src_connection.number

MutationObject = Union[WeightMutation, BiasMutation, ConnectionMutation, NodeMutation]
