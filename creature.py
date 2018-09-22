# creature.py
# Description: creature object.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from dna import Dna, List
from network import Network
from constants import COLOR

# Constants
WEIGHT_RANGE = 2.0


class Creature:

    def __init__(self, inputs: int = None, outputs: int = None, colors: List[COLOR] = None, dna: Dna = None,
                 name='Creature', weight_range: float = WEIGHT_RANGE):

        # Take dna inputs & outputs if dna is given, else take values.
        self.inputs = dna.inputs if dna is not None else inputs
        self.outputs = dna.outputs if dna is not None else outputs
        self.name = name

        self.weight_range = weight_range

        self.dna = dna if dna is not None else Dna(self.inputs, self.outputs, self.weight_range)
        self.network = Network(self.dna.nodes, self.dna.node_connections)

        # Outline how to draw the shape.
        # For example body = [[(0, 0, 100, 100)], [(0, 100, 20, 20)]]
        # The first list is all ellipses with the PRIMARY color, [(0, 0, 100, 100)].
        # The second list is all ellipses with the SECONDARY color, [(0, 100, 20, 20)]. And so on and so forth.
        if colors is None:
            colors = list()
        self.colors = colors
        self.body = [[(0, 0, 100, 100)], [(0, 100, 25, 25)]]

    def think(self, inputs: List[float]) -> List[float]:
        """
        Gets the creature decision based on the inputs it was given.
        :param inputs: Sensory input.
        :return: Creature decision.
        """
        return self.network.get_output(inputs)

if __name__ == '__main__':
    from node import *
    from connection import Connection
    nodes = {0: InputNode(0),
             1: HiddenNode(1, 2),
             2: OutputNode(2, 2)}
    connections = {0: Connection(number=0, src_number=0, dst_number=1, weight_range=2),
                   1: Connection(number=1, src_number=1, dst_number=2, weight_range=2),
                   2: Connection(number=2, src_number=2, dst_number=1, weight_range=2)}
    dna = Dna(inputs=2, outputs=1, weight_range=2, nodes=nodes, connections=connections)
    c = Creature(dna=dna)
    print(c.think([1]))
    print(c.think([0]))
    print(c.dna)

