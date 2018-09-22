# main.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
import collections
import sys
from typing import Union

import pygame
from pygame import gfxdraw

# Constants
from creature import Creature
from my_types import COLOR, GraphicInfo, CreatureInfo

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

    def __init__(self, population_size: int, creature_inputs: int, creature_outputs: int):
        self.population_size = population_size
        self.population = dict()
        self.graphics = dict()
        for _ in range(population_size):
            creature = Creature(creature_inputs, creature_outputs, weight_range=WEIGHT_RANGE, colors=[BLUE, RED])
            self.population[creature] = CreatureInfo()
            self.graphics[creature] = GraphicInfo(300, 200, 0.2)

    def update(self) -> None:
        """
        Runs a single frame of the simulation.
        """


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Creatures')
    clock = pygame.time.Clock()
    run = True
    simulation = Simulation(1, 2, 1)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill(BACKGROUND)
        simulation.update()
        for obj in simulation.graphics:
            draw_object(screen, obj, *simulation.graphics[obj])
        pygame.display.update()
        clock.tick()
    sys.exit(1)
