# node.py
# Description: node objects for network.
# ---------------------------------------------------------------------------------------
import math
import random
from abc import ABC, abstractmethod
from typing import Callable

# Constants
STRING = "{} {}"


# Activation function
def sigmoid(x: float) -> float:
	return 1.0 / (1.0 + pow(math.e, -x))


class BaseNode(ABC):

	def __init__(self, number: int, activation: Callable[[float], float] = sigmoid):
		self.number = number
		self.activation = activation
		self.name = self.__class__.__name__

	def __str__(self):
		return STRING.format(self.name, self.number)

	def __repr__(self):
		return str(self)

	@abstractmethod
	def get_output(self) -> float:
		pass

	@abstractmethod
	def add_input(self, input_value: float) -> None:
		pass

	@abstractmethod
	def reset_node(self) -> None:
		pass


class InputNode(BaseNode):

	def __init__(self, number: int, activation: Callable[[float], float] = sigmoid):
		super(InputNode, self).__init__(number, activation)
		self.output = self.inputs = 0

	def get_output(self) -> float:
		return self.output

	def add_input(self, input_value: float) -> None:
		self.inputs = self.output = input_value

	def reset_node(self) -> None:
		self.inputs = self.output = 0


class HiddenNode(BaseNode):

	def __init__(self, number: int, bias_range: float, activation: Callable[[float], float] = sigmoid):
		super(HiddenNode, self).__init__(number, activation)
		self.bias = random.random() * bias_range * 2 - bias_range
		self.inputs = []
		self.output = 0

	def get_output(self) -> float:
		self.output = self.activation(sum(self.inputs)) + self.bias
		return self.output

	def add_input(self, input_value: float) -> None:
		self.inputs.append(input_value)

	def reset_node(self) -> None:
		self.inputs = []
		self.output = 0


class OutputNode(HiddenNode):
	"""
	OutputNode is the same as HiddenNode, here for easy recognition of output nodes later on.
	"""

	def __init__(self, number: int, bias: float, activation: Callable[[float], float] = sigmoid):
		super(OutputNode, self).__init__(number, bias, activation)

if __name__ == '__main__':
	inn = InputNode(0)
	hid = HiddenNode(1, 0)
	out = OutputNode(2, 0)

	print(inn, hid, out)

	inn.add_input(432)
	print("inn output:", inn.get_output())

	hid.add_input(inn.get_output())
	print("hid output:", hid.get_output())

	out.add_input(hid.get_output())
	print("out output:", out.get_output())