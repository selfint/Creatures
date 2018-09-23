# simulation.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from random import randint, choice
from typing import Union

import pygame
from pygame import gfxdraw

# Constants
from constants import COLOR, CreatureInfo, CREATURE_COLORS, CreatureNetworkInput
from creature import Creature

HEIGHT = 600
WIDTH = 800
BLACK = 0, 0, 0
GREY = 125, 125, 125
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
BACKGROUND = 230, 220, 50

CENTER = 0
WEIGHT_RANGE = 2.0


def ellipse(screen: object, x: float, y: float, width: float, height: float,
            color: COLOR = None, stroke: COLOR = BLACK, mode:int = CENTER) -> None:
    """
    Draw an anti-aliased ellipse onto the screen.
    :param stroke: Edge color of the ellipse.
    :param mode: Where to draw the ellipse from.
    :return:
    """

    # Default color is GREY with BLACK stroke
    if color is None:
        color = GREY
    if stroke is None:
        stroke = BLACK

    # Draw ellipse.
    if mode == CENTER:
        pygame.gfxdraw.filled_ellipse(screen, int(x), int(y), int(width), int(height), color)
        pygame.gfxdraw.aaellipse(screen, int(x), int(y), int(width), int(height), stroke)


def draw_creature(screen: object, creature: Creature, x: float, y: float, scale: float) -> None:
    """
    Parses creature body data and draws it onto the screen.
    :param scale: Changes the size of the creature.
    :param colors: Color theme for creature, will be treated as primary and secondary color.
    """

    # Get creature body data.
    for i in range(len(creature.body)):
        shapes = creature.body[i]
        for shape_x, shape_y, shape_width, shape_height in shapes:
            if i < len(creature.colors):
                shape_color = creature.colors[i]
            else:
                shape_color = None
            ellipse(screen, x + shape_x*scale, y + shape_y*scale, scale * shape_width, scale * shape_height,
                    shape_color)


def draw_object(screen: object, thing: Union[Creature], x:float, y:float, scale:float) -> None:
    """
    Calls the appropriate function based on the object type. Assumes the object has Info tuple
    """

    if isinstance(thing, Creature):
        draw_creature(screen, thing, x, y, scale)


class Simulation:

    def __init__(self, population_size: int, creature_inputs: int, creature_outputs: int,
                 width: int = WIDTH, height: int = HEIGHT):
        self.population_size = population_size
        self.population = dict()
        self.world_width = width
        self.world_height = height
        for i in range(population_size):
            primary = choice(list(CREATURE_COLORS.values()))
            secondary = choice(list(color for color in CREATURE_COLORS.values() if color is not primary))
            creature = Creature(creature_inputs, creature_outputs,
                                colors=[primary, secondary], weight_range=WEIGHT_RANGE, name=str(i))
            self.population[creature] = CreatureInfo(randint(0, self.world_width), randint(0, self.world_height), 0.2)
        self.world_info = self.population

    def update(self) -> None:
        """
        Runs a single frame of the simulation.
        """
        for creature, creature_info in self.population.items():
            creature_decisions = []
            for other, other_info in self.world_info.items():
                creature_decision = creature.think(self.info_to_vec(creature_info, other_info))
                creature_decisions.append(creature_decision)
            print(creature_decisions)

    def info_to_vec(self, creature_info: CreatureInfo, other_info: CreatureInfo) -> CreatureNetworkInput:
        """
        Meaningfully convert CreatureInfo of a target creature to a vector,
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
