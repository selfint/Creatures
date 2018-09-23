# mutations.py
# Description: All possible mutation types.
# ---------------------------------------------------------------------------------------

# Imports
from abc import ABC, abstractmethod
from random import random

# Constants
from Constants.neat_parameters import WEIGHT_RANGE, BIAS_RANGE
from Constants.types import NodeObject
from connection import Connection
from node import HiddenNode


class BaseMutation(ABC):

    def __init__(self, number: int, *args):
        self.number = number

class WeightMutation(BaseMutation):

    def __init__(self, number: int, connection: Connection, pertrube_rate: float, pertrube_amount: float,
                 weight_range: float = WEIGHT_RANGE):
        super(WeightMutation, self).__init__(number)
        self.connection = connection
        if random() < pertrube_rate:
            self.new_weight = self.connection.weight + (random() * 2 - 1) * pertrube_amount
        else:
            self.new_weight = random() * weight_range * 2 - weight_range

class BiasMutation(BaseMutation):

    def __init__(self, number: int, node: NodeObject, pertrube_rate: float, pertrube_amount: float,
                 bias_range: float = BIAS_RANGE):
        super(BiasMutation, self).__init__(number)
        self.node = node
        if random() < pertrube_rate:
            self.new_bias = self.node.bias + (random() * 2 - 1) * pertrube_amount
        else:
            self.new_bias = random() * bias_range * 2 - bias_range

class ConnectionMutation(BaseMutation):

    def __init__(self, number: int, source_number: int, dest_number: int, weight_range:float = WEIGHT_RANGE):
        super(ConnectionMutation, self).__init__(number)
        self.source_number = source_number
        self.dest_number = dest_number
        self.connection = Connection(None, self.source_number, self.dest_number, weight_range)

class NodeMutation(BaseMutation):

    def __init__(self, number:int, connection: Connection, weight_range:float = WEIGHT_RANGE):
        super(NodeMutation, self).__init__(number)
        self.old_connection = connection

        # src----old_connection--->dst
        # src-dst_conn->new_node->src_conn->dst
        # Connection that has new_node as DST.
        self.new_dst_connection = Connection(None, self.old_connection.src_number, None, weight_range)
        self.new_node = HiddenNode(None, BIAS_RANGE)

        # Connection that has new_node as SRC.
        self.new_src_connection = Connection(None, None, self.old_connection.dst_number, weight_range)

