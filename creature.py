# creature.py
# Description: creature object.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import List, Union

# Constants
from Constants.data_structures import CreatureNetworkInput, CreatureNetworkOutput
from Constants.types import COLOR
# Objects
from dna import Dna
from mutations import BaseMutation, NumberedMutation
from network import Network


class Creature:

    def __init__(self, inputs: int = None, outputs: int = None, colors: List[COLOR] = None, dna: Dna = None,
                 name='Creature'):

        # Take dna inputs & outputs if dna is given, else take values.
        self.inputs = dna.inputs if dna is not None else inputs
        self.outputs = dna.outputs if dna is not None else outputs
        self.name = name

        self.dna = dna if dna is not None else Dna(self.inputs, self.outputs)
        self.network = Network(self.dna.nodes, self.dna.node_connections)

        # Outline how to draw the shape.
        # For example body = [[(0, 0, 100, 100)], [(0, 100, 20, 20)]]
        # The first list is all ellipses with the PRIMARY color, [(0, 0, 100, 100)].
        # The second list is all ellipses with the SECONDARY color, [(0, 100, 20, 20)]. And so on and so forth.
        if colors is None:
            colors = list()
        self.colors = colors
        self.body = [[(0, 0, 100, 100)], [(0, 100, 25, 25)]]

    def think(self, inputs: CreatureNetworkInput) -> CreatureNetworkOutput:
        """
        Gets the creature decision based on the inputs it was given.
        :param inputs: Sensory input.
        :return: Creature decision.
        """
        return CreatureNetworkOutput(*self.network.get_output(list(inputs)))

    def update(self, mutations: List[Union[BaseMutation, NumberedMutation]]):
        self.dna.update(mutations)
        self.network = Network(self.dna.nodes, self.dna.node_connections)


if __name__ == '__main__':
    from node import *
    from connection import Connection

    nodes = {0: InputNode(0),
             1: HiddenNode(1, 2),
             2: OutputNode(2, 2)}
    connections = {0: Connection(number=0, src_number=0, dst_number=1),
                   1: Connection(number=1, src_number=1, dst_number=2),
                   2: Connection(number=2, src_number=2, dst_number=1)}
    dna = Dna(inputs=2, outputs=1, nodes=nodes, connections=connections)
    c = Creature(dna=dna)
    print(c.think([1]))
    print(c.think([0]))
    print(c.dna)

