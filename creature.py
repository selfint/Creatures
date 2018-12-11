# creature.py
# Description: creature object.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import List, Union

# Constants
from Constants.constants import CREATURE_STRING, CREATURE_BODY, CREATURE_REACH, CREATURE_LINE_OF_SIGHT
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
        self.age = 0
        self.distance_travelled = 0
        self.network = Network(self.dna.nodes, self.dna.node_connections)

        if colors is None:
            colors = list()
        self.colors = colors
        self.body = CREATURE_BODY

        # Creature attributes.
        self.name = generate_name()
        self.fitness = 0
        self.health = CREATURE_HEALTH
        self.reach = CREATURE_REACH
        self.line_of_sight = CREATURE_LINE_OF_SIGHT

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
    main_dna = Dna(inputs=2, outputs=6)
    c = Creature(dna=main_dna)
    print(c.think(CreatureNetworkInput(0, 0, 0)))
    print(c.think(CreatureNetworkInput(100, 100, 100)))
