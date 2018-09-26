# mutations.py
# Description: All possible mutation types.
# ---------------------------------------------------------------------------------------

# Imports
from abc import ABC
from random import random
from typing import Union

# Constants
from Constants.constants import BASE_MUTATION_STRING, WEIGHT_MUTATION_STRING, BIAS_MUTATION_STRING, NODE_MUTATION_STRING
from Constants.neat_parameters import WEIGHT_RANGE, BIAS_RANGE
from Constants.types import NodeObject
from connection import Connection
from node import HiddenNode

class BaseMutation(ABC):

    def __init__(self, number: Union[int, None]):
        self.number = number
        self.name = self.__class__.__name__
        self.string = ''

    def __str__(self):
        return BASE_MUTATION_STRING.format(self.name, self.number, self.string)

    def __repr__(self):
        return str(self)


class WeightMutation(BaseMutation):

    def __init__(self, number: None, connection: Connection, pertrub_rate: float, pertrub_amount: float,
                 weight_range: float = WEIGHT_RANGE):
        super(WeightMutation, self).__init__(number)
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

    def __init__(self, number: None, node: NodeObject, pertrub_rate: float, pertrub_amount: float,
                 bias_range: float = BIAS_RANGE):
        super(BiasMutation, self).__init__(number)
        self.node = node
        name, number, bias = node.name, node.number, node.bias

        # Randomly choose between perturbing the bias or completely changing it.
        if random() < pertrub_rate:
            self.new_bias = self.node.bias + (random() * 2 - 1) * pertrub_amount
        else:
            self.new_bias = random() * bias_range * 2 - bias_range

        # Generate mutation string.
        self.string = BIAS_MUTATION_STRING.format(name, number, bias, self.new_bias)


class ConnectionMutation(BaseMutation):

    def __init__(self, number: Union[int, None], source_number: Union[int, None],
                 dest_number: Union[int, None], weight_range:float = WEIGHT_RANGE):
        super(ConnectionMutation, self).__init__(number)
        self.source_number = source_number
        self.dest_number = dest_number
        self.connection = Connection(None, self.source_number, self.dest_number, weight_range)
        self.string = str(self.connection)

class NodeMutation(BaseMutation):

    def __init__(self, number: Union[int, None], connection: Connection, weight_range:float = WEIGHT_RANGE):
        super(NodeMutation, self).__init__(number)
        self.old_connection = connection
        old_src, old_dst, old_weight = connection.src_number, connection.dst_number, connection.weight

        # The number of the connection this node split, will be used to identify identical node mutations.
        self.connection_number = connection.number

        # src----old_connection--->dst
        # src-dst_conn->new_node->src_conn->dst
        # Connection that has new_node as DST.
        self.new_dst_connection = Connection(None, old_src, None, weight=1)
        self.new_node = HiddenNode(None, BIAS_RANGE)

        # Connection that has new_node as SRC.
        self.new_src_connection = Connection(None, None, old_dst, weight=old_weight)

        self.string = NODE_MUTATION_STRING.format(self.new_dst_connection.src_number, self.new_dst_connection.weight,
                                                  self.new_node.number, self.new_src_connection.weight,
                                                  self.new_src_connection.dst_number)



