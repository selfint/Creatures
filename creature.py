# creature.py
# Description: creature object.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import List, Union

# Constants
from Constants.constants import CREATURE_STRING, CREATURE_BODY
from Constants.data_structures import CreatureNetworkInput, CreatureNetworkOutput
from Constants.neat_parameters import CREATURE_HEALTH
from Constants.types import COLOR
# Objects
from dna import Dna
from functions import generate_name
from mutations import MutationObject
from network import Network


class Creature:

    def __init__(self, dna: Dna, colors: List[COLOR] = None):
        self.inputs = dna.inputs
        self.outputs = dna.outputs
        self.dna = dna
        self.network = Network(self.dna.nodes, self.dna.node_connections)

        if colors is None:
            colors = list()
        self.colors = colors
        self.body = CREATURE_BODY

        # Creature attributes.
        self.name = generate_name()
        self.fitness = 0
        self.health = CREATURE_HEALTH

    def __str__(self):
        return CREATURE_STRING.format(self.name, self.dna.hidden)

    def __repr__(self):
        return str(self)

    def think(self, inputs: CreatureNetworkInput) -> CreatureNetworkOutput:
        """
        Gets the creature decision based on the inputs it was given.
        :param inputs: Sensory input.
        :return: Creature decision.
        """
        return CreatureNetworkOutput(*self.network.get_output(list(inputs)))

    def update(self, mutations: List[Union[MutationObject]]):
        self.dna.update(mutations)
        self.network = Network(self.dna.nodes, self.dna.node_connections)


if __name__ == '__main__':
    from node import *
    from connection import Connection

    main_nodes = {0: InputNode(0),
                  1: HiddenNode(1, 2),
                  2: OutputNode(2, 2)}
    main_connections = {0: Connection(number=0, src_number=0, dst_number=1),
                        1: Connection(number=1, src_number=1, dst_number=2),
                        2: Connection(number=2, src_number=2, dst_number=1)}
    main_dna = Dna(inputs=2, outputs=1, nodes=main_nodes, connections=main_connections)
    c = Creature(dna=main_dna)
    print(c.think([1]))
    print(c.think([0]))
    print(c.dna)
