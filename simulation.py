# simulation.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from random import randint, choice

# Constants
from Constants.constants import WIDTH, HEIGHT, CREATURE_COLORS
from Constants.data_structures import CreatureInfo, CreatureNetworkInput
from Constants.neat_parameters import WEIGHT_RANGE
# Objects
from creature import Creature


class Simulation:

    def __init__(self, population_size: int, creature_inputs: int, creature_outputs: int,
                 width: int = WIDTH, height: int = HEIGHT):
        self.population_size = population_size
        self.population = dict()
        self.world_width = width
        self.world_height = height

        # Map creatures to creature info named tuples.
        for i in range(population_size):

            # Generate random colors, add species-based colors later.
            primary = choice(list(CREATURE_COLORS.values()))
            secondary = choice(list(color for color in CREATURE_COLORS.values() if color is not primary))

            # Generate creature and creature info.
            creature = Creature(creature_inputs, creature_outputs,
                                colors=[primary, secondary], weight_range=WEIGHT_RANGE, name=str(i))
            creature_info = CreatureInfo(randint(0, self.world_width), randint(0, self.world_height), 0.2)
            self.population[creature] = creature_info

        # Add all object in the world and their info into the world info dictionary.
        self.world_info = self.population

    def update(self) -> None:
        """
        Runs a single frame of the simulation.
        """

        # Get creature's thoughts about all other creatures.
        for creature, creature_info in self.population.items():
            creature_decisions = [creature.think(self.info_to_vec(creature_info, other_info))
                                  for other, other_info in self.world_info.items() if other is not creature]
            print(creature_decisions)

    def info_to_vec(self, creature_info: CreatureInfo, other_info: CreatureInfo) -> CreatureNetworkInput:
        """
        Meaningfully convert CreatureInfo of a target creature to a CreatureNetworkInput named tuple,
        based on the creature info of the source creature.
        :param creature_info: Source creature (creature LOOKING).
        :param other_info: Destination creature (creature SEEN).
        :return: Network input for creature LOOKING at creature SEEN.
        """

        # Calculate dx and dy.
        dx = (creature_info.x - other_info.x) / self.world_width
        dy = (creature_info.y - other_info.y) / self.world_height

        # Build network input.
        network_input = CreatureNetworkInput(dx, dy)
        return network_input


if __name__ == '__main__':
    s = Simulation(2, 2, 4)
    c1, c2 = s.population.values()
    s.info_to_vec(c1, c2)
