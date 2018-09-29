# simulation.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from random import randint, choice, random
from typing import List, Union, Dict

# Constants
from Constants.constants import WIDTH, HEIGHT, CREATURE_COLORS, SPEED_SCALING
from Constants.data_structures import CreatureInfo, CreatureNetworkInput, CreatureNetworkOutput, CreatureActions
from Constants.neat_parameters import WEIGHT_MUTATION_RATE, BIAS_MUTATION_RATE, \
    CONNECTION_MUTATION_RATE, NODE_MUTATION_RATE, CREATURE_OUTPUTS, CREATURE_INPUTS
# Objects
from creature import Creature
from functions import clamp, split_by_type, flatten
from mutations import WeightMutation, BiasMutation, ConnectionMutation, NodeMutation, NumberedMutation, BaseMutation, MutationObject


class Simulation:

    def __init__(self, population_size: int, creature_inputs: int, creature_outputs: int,
                 width: int = WIDTH, height: int = HEIGHT):
        self.population_size = population_size
        self.population = dict()
        self.world_width = width
        self.world_height = height
        self.node_count = creature_inputs + creature_outputs - 1
        self.connection_count = creature_inputs * creature_outputs - 1

        # All attributes that can be changed in creature info
        self.creature_actions = 'x', 'y'

        # Map creatures to creature info named tuples.
        for i in range(population_size):

            # Generate random colors, add species-based colors later.
            primary = choice(list(CREATURE_COLORS.values()))
            secondary = choice(list(color for color in CREATURE_COLORS.values() if color is not primary))

            # Generate creature and creature info.
            creature = Creature(creature_inputs, creature_outputs, colors=[primary, secondary], name=str(i))
            creature_info = CreatureInfo(randint(0, self.world_width), randint(0, self.world_height), 0.2)
            self.population[creature] = creature_info

        # Add all connections to mutation history.
        self.mutation_history = []
        self.connection_count = 0
        temp = list(self.population.keys())[0]
        connections = temp.dna.connections.values()
        for conn in connections:
            self.mutation_history.append(ConnectionMutation(connection=conn))

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

    def weight_mutation(self, creature: Creature) -> WeightMutation:
        """
        Return a weight mutation object from the creature. A weight mutation has no number, the object is here
        for organization purposes. ALWAYS returns a mutation, random chance is handle in simulation.mutate().
        """

        # Choose random connection.
        connection = choice(list(creature.dna.connections.values()))

        # Generate random weight mutation.
        mutation = WeightMutation(connection)
        return mutation

    def bias_mutation(self, creature: Creature) -> BiasMutation:
        """
        Return a weight mutation object from the creature. A weight mutation has no number, the object is here
        for organization purposes. ALWAYS returns a mutation, random chance is handle in simulation.mutate().
        """

        # Choose random node.
        node = choice(list(creature.dna.nodes.values()))

        # Generate random weight mutation.
        mutation = BiasMutation(node)
        return mutation

    def connection_mutation(self, creature: Creature) -> ConnectionMutation:
        """
        Returns a new old_connection mutation based on the creature.
        """

        # Get all creature dna's nodes and connections.
        available_connections = creature.dna.available_connections()

        # Choose random connection to generate.
        src, dst = choice(available_connections)

        # Generate new connection between nodes.
        mutation = ConnectionMutation(None, src, dst)
        return mutation

    def node_mutation(self, creature: Creature) -> NodeMutation:
        """
        Returns a new node mutation based on the creature.
        """

        # Choose a random connection to split.
        connection = choice(list(creature.dna.connections.values()))

        # Generate node mutation.
        mutation = NodeMutation(None, connection)
        return mutation

    def mutate(self, creature: Creature) -> List[Union[BaseMutation, NumberedMutation]]:
        """
        Get mutations based on the creature, based on random chance and neat_parameter values.
        """
        mutations = []

        # Weight and bias mutations.
        if random() < WEIGHT_MUTATION_RATE and creature.dna.connections:
            mutations.append(self.weight_mutation(creature))
        if random() < BIAS_MUTATION_RATE and creature.dna.nodes:
            mutations.append(self.bias_mutation(creature))

        # Check if a connection is possible if random wants to mutate a connection.
        if creature.dna.available_connections(shallow=True) and random() < CONNECTION_MUTATION_RATE:
            mutations.append(self.connection_mutation(creature))

        # Node mutation.
        if random() < NODE_MUTATION_RATE and creature.dna.connections:
            mutations.append(self.node_mutation(creature))

        return mutations

    def apply_mutations(self, creature: Creature, mutations: List[MutationObject]) -> None:
        """
        Applies mutation to creature's dna.
        """
        creature.update(mutations)

    def new_creatures(self, amount: int) -> List[Creature]:
        """
        Generate new creatures.
        """
        children = [self.new_child() for _ in range(amount)]
        children_mutations = self.generate_mutations(children)
        for child in children:
            self.apply_mutations(child, children_mutations[child])
        return children

    def generate_mutations(self, creatures: List[Creature]) -> Dict[Creature, List[MutationObject]]:
        """
        Generates mutations for all new creatures, and configures them.
        :return: All mutations for each creature.
        """

        # Generate mutations.
        creature_mutations = {creature: self.mutate(creature) for creature in creatures}
        mutations = flatten(list(creature_mutations.values()))
        numbered_mutations = [mutation for mutation in mutations if isinstance(mutation, NumberedMutation)]

        # Configure mutations.
        for mutation in numbered_mutations:
            for past_mutation in self.mutation_history:
                if mutation.unique() == past_mutation.unique():
                    mutation.configure(past_mutation.configurations())
                    break
            # If no mutations were matching in past mutations.
            else:
                self.connection_count, self.node_count = mutation.calc_configurations(self.connection_count,
                                                                                      self.node_count)

        return creature_mutations

    def new_child(self) -> Creature:
        """
        Generate a new creature. Add call to crossover here.
        """
        child = Creature(CREATURE_INPUTS, CREATURE_OUTPUTS)
        return child


if __name__ == '__main__':
    s = Simulation(2, 2, 5)
    c1, c2 = s.population.keys()
    ci1, ci2 = s.population.values()
    print(s.new_creatures(5))
