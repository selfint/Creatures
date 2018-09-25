# node.py
# Description: node objects for network.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import math
import random
from abc import ABC, abstractmethod
from typing import Callable, List, Union

# Constants
from Constants.constants import NODE_STRING


# Activation function
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + pow(math.e, -x))


class BaseNode(ABC):

    def __init__(self, number: int, activation: Callable[[float], float] = sigmoid):
        self.number = number
        self.activation = activation
        self.name = self.__class__.__name__
        self.bias = 0
        self.reset_node()

    def __str__(self):
        return NODE_STRING.format(self.name, self.number, self.bias)

    def __repr__(self):
        return str(self)

    @abstractmethod
    def get_output(self) -> float:
        pass

    @abstractmethod
    def set_input(self, input_value: float) -> None:
        pass

    def reset_node(self) -> None:
        self.inputs = self.output = None


class InputNode(BaseNode):

    def __init__(self, number: int, activation: Callable[[float], float] = sigmoid):
        super(InputNode, self).__init__(number, activation)
        self.reset_node()

    def get_output(self) -> float:
        return self.output

    def set_input(self, input_value: float) -> None:
        """
        Sets the nodes input only if the input has not been set. To change an inputs node input, you must reset it.
        """
        self.inputs = self.output = input_value if self.inputs is None else self.inputs


class HiddenNode(BaseNode):

    def __init__(self, number: Union[int, None], bias_range: float, activation: Callable[[float], float] = sigmoid):
        super(HiddenNode, self).__init__(number, activation)
        self.bias = random.random() * bias_range * 2 - bias_range
        self.reset_node()

    def get_output(self) -> float:
        self.output = self.activation(sum(self.inputs)) + self.bias
        return self.output

    def set_input(self, input_value: List[float]) -> None:
        self.inputs = input_value


class OutputNode(HiddenNode):
    """
    OutputNode is the same as HiddenNode, here for easy recognition of output nodes later on.
    """

    def __init__(self, number: int, bias: float, activation: Callable[[float], float] = sigmoid):
        super(OutputNode, self).__init__(number, bias, activation)


if __name__ == '__main__':
    inn = InputNode(0)
    hid = HiddenNode(1, 3)
    out = OutputNode(2, 2)

    print(inn, hid, out)

    inn.set_input(432)
    print("inn output:", inn.get_output())

    hid.set_input([inn.get_output()])
    print("hid output:", hid.get_output())

    out.set_input([hid.get_output()])
    print("out output:", out.get_output())