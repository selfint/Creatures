# simulation.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from random import randint, choice

# Constants
from typing import List

from Constants.constants import WIDTH, HEIGHT, CREATURE_COLORS, SPEED_SCALING
from Constants.data_structures import CreatureInfo, CreatureNetworkInput, CreatureNetworkOutput, CreatureActions
from Constants.neat_parameters import WEIGHT_RANGE
# Objects
from creature import Creature
from functions import clamp


class Simulation:

    def __init__(self, population_size: int, creature_inputs: int, creature_outputs: int,
                 width: int = WIDTH, height: int = HEIGHT):
        self.population_size = population_size
        self.population = dict()
        self.world_width = width
        self.world_height = height

        # All attributes that can be changed in creature info
        self.creature_actions = 'x', 'y'

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
            creature_actions = self.interpret_decisions(creature_decisions)
            self.apply_action(creature, creature_actions)
        self.constrain_creatures()

    def apply_action(self, creature: Creature, creature_actions: CreatureActions) -> None:
        """
        Applies the action the creature decided to do.
        """
        info = self.population[creature]
        for attr in self.creature_actions:
            creature_attr, action_attr = getattr(info, attr), getattr(creature_actions, attr)
            setattr(info, attr, creature_attr + action_attr)

    def interpret_decisions(self, decisions: List[CreatureNetworkOutput]) -> CreatureActions:
        """
        Converts creature network output to creature actions.
        :param decisions: All decisions creature made towards all other creatures.
        """

        # Avg out everything the creature wants to do, using a weighted average against the urgency of each decision.
        move_x, move_y = 0, 0
        for decision in decisions:
            left, right, up, down, urgency = decision
            if right > left:
                move_x += right * urgency
            elif right < left:
                move_x += -left * urgency
            if up > down:
                move_y += up * urgency
            elif up < down:
                move_y += -down * urgency
        if decisions:
            move_x = move_x * SPEED_SCALING / len(decisions)
            move_y = move_y * SPEED_SCALING / len(decisions)

        actions = CreatureActions(move_x, move_y)
        return actions

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

    def constrain_creatures(self, x_min: int = 0, y_min: int = 0, x_max: int = WIDTH, y_max: int = HEIGHT) -> None:
        """
        Makes sure all creatures stay within given borders (default is screen size).
        """
        for creature_info in self.population.values():
            creature_info.x = clamp(creature_info.x, x_min, x_max)
            creature_info.y = clamp(creature_info.y, y_min, y_max)

    def weight_mutation(self, creature: Creature):
        """
        Return a weight mutation object from the creature. A weight mutation has no number, the object is here
        for organization purposes.
        """

    def connection_mutation(self, creature: Creature):
        """
        Returns a new old_connection mutation based on the creature.
        """

    def node_mutation(self, creature: Creature):
        """
        Returns a new node mutation based on the creature.
        """

    def mutate(self, creature: Creature):
        """
        Get mutations based on the creature, based on random chance and neat_parameter values.
        """

if __name__ == '__main__':
    s = Simulation(2, 2, 4)
    c1, c2 = s.population.values()
    s.info_to_vec(c1, c2)
