# mutations.py
# Description: All possible mutation types.
# ---------------------------------------------------------------------------------------

# Imports
from abc import ABC, abstractmethod
from random import random
from typing import Union

# Constants
from Constants.constants import NUMBERED_MUTATION_STRING, WEIGHT_MUTATION_STRING, BIAS_MUTATION_STRING, \
    NODE_MUTATION_STRING, BASE_MUTATION_STRING
from Constants.neat_parameters import WEIGHT_RANGE, BIAS_RANGE
from Constants.types import NodeObject
from connection import Connection
from node import HiddenNode


class BaseMutation(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        self.string = ''

    def __str__(self):
        return BASE_MUTATION_STRING.format(self.name, self.string)

    def __repr__(self):
        return str(self)


class NumberedMutation(BaseMutation):

    def __init__(self, number: Union[int, None]):
        super(NumberedMutation, self).__init__()
        self.number = number

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


class WeightMutation(BaseMutation):

    def __init__(self, connection: Connection, pertrub_rate: float, pertrub_amount: float,
                 weight_range: float = WEIGHT_RANGE):
        super(WeightMutation, self).__init__()
        self.connection = connection
        number, src, weight, dst = connection.number, connection.src_number, connection.weight, connection.dst_number

        # Randomly choose between perturbing the weight or completely changing it.
        if random() < pertrub_rate:
            self.new_weight = weight + (random() * 2 - 1) * pertrub_amount
        else:
            self.new_weight = random() * weight_range * 2 - weight_range

        # Generate mutation string.
        self.string = WEIGHT_MUTATION_STRING.format(number, src, weight, self.new_weight, dst)


class BiasMutation(BaseMutation):

    def __init__(self, node: NodeObject, pertrub_rate: float, pertrub_amount: float,
                 bias_range: float = BIAS_RANGE):
        super(BiasMutation, self).__init__()
        self.node = node
        name, number, bias = node.name, node.number, node.bias

        # Randomly choose between perturbing the bias or completely changing it.
        if random() < pertrub_rate:
            self.new_bias = self.node.bias + (random() * 2 - 1) * pertrub_amount
        else:
            self.new_bias = random() * bias_range * 2 - bias_range

        # Generate mutation string.
        self.string = BIAS_MUTATION_STRING.format(name, number, bias, self.new_bias)


class ConnectionMutation(NumberedMutation):

    def __init__(self, number: Union[int, None], source_number: Union[int, None],
                 dst_number: Union[int, None], weight_range:float = WEIGHT_RANGE):
        super(ConnectionMutation, self).__init__(number)
        self.src_number = source_number
        self.dst_number = dst_number
        self.connection = Connection(None, self.src_number, self.dst_number, weight_range)
        self.set_string()

    def set_string(self) -> None:
        self.string = str(self.connection)

    def configure(self, number: int = None, src_number: int = None, dst_number: int = None) -> None:
        self.number = number or self.number
        self.src_number = src_number or self.src_number
        self.dst_number = dst_number or self.dst_number
        self.set_string()


class NodeMutation(NumberedMutation):

    def __init__(self, number: Union[int, None], connection: Connection):
        super(NodeMutation, self).__init__(number)
        self.old_connection = connection

        # Disable connection that is being split.
        self.old_connection.enabled = False
        old_src, old_dst, old_weight = connection.src_number, connection.dst_number, connection.weight

        # The number of the connection this node split, will be used to identify identical node mutations.
        self.connection_number = connection.number

        # src----old_connection--->dst
        # src-dst_conn->new_node->src_conn->dst
        # Connection that has new_node as DST.
        self.new_node = HiddenNode(None, BIAS_RANGE)
        self.new_dst_connection = Connection(None, old_src, self.new_node.number, weight=1)

        # Connection that has new_node as SRC.
        self.new_src_connection = Connection(None, self.new_node.number, old_dst, weight=old_weight)
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

