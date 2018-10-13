# graphics.py
# Description: graphic representation of the simulation.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import Union

# Pygame
import pygame
from pygame import gfxdraw

# Constants
from Constants.constants import BACKGROUND, BLACK, CENTER, FRAME_RATE, GREY, RED, SIMULATION_BACKGROUND
from Constants.types import COLOR
# Objects
from creature import Creature
from simulation import Simulation


def ellipse(screen: object, x: float, y: float, width: float, height: float,
            color: COLOR = None, stroke: COLOR = BLACK, mode: int = CENTER) -> None:
    """
    Draw an anti-aliased ellipse onto the screen.
    :param stroke: Edge color of the ellipse.
    :param mode: Where to draw the ellipse from.
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
            ellipse(screen, x + shape_x * scale, y + shape_y * scale, scale * shape_width, scale * shape_height,
                    shape_color)


def draw_object(screen: object, thing: Union[Creature], x: float, y: float, scale: float) -> None:
    """
    Calls the appropriate function based on the object type. Assumes the object has Info tuple
    """

    # Draw Creatures.
    if isinstance(thing, Creature):
        draw_creature(screen, thing, x, y, scale)


class Graphics:

    def __init__(self, simulation: Simulation, width: int, height: int, caption: str):
        """
        Renders the simulation.
        """
        self.simulation = simulation
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        # Setup camera.
        self.camera_window_x = 0
        self.camera_window_y = 0
        self.camera_dx, self.camera_dy = 0, 0
        self.camera = {'x': self.camera_window_x, 'y': self.camera_window_y,
                       'w': self.width / 2.0, 'h': self.height / 2.0}

    def run(self) -> None:
        """
        Runs graphics.
        """
        pygame.init()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Camera movement.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.camera_dx = -1
                    elif event.key == pygame.K_UP:
                        self.camera_dy = -1
                    elif event.key == pygame.K_RIGHT:
                        self.camera_dx = 1
                    elif event.key == pygame.K_DOWN:
                        self.camera_dy = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.camera_dx = 0
                    elif event.key == pygame.K_UP:
                        self.camera_dy = 0
                    elif event.key == pygame.K_RIGHT:
                        self.camera_dx = 0
                    elif event.key == pygame.K_DOWN:
                        self.camera_dy = 0
            self.camera['x'] += self.camera_dx
            self.camera['y'] += self.camera_dy

            # Draw screen shapes.
            self.screen.fill(BACKGROUND)
            self.draw_simulation_background()

            # Run simulation.
            self.simulation.update()
            for obj in self.simulation.world_info:
                object_info = self.simulation.world_info[obj]

                # Make sure object is in view of the camera.
                if self.in_view(object_info.x, object_info.y):
                    draw_object(self.screen, obj,
                                object_info.x - self.camera['x'],
                                object_info.y - self.camera['y'],
                                object_info.scale)
            self.draw_camera()

            # Update frame.
            pygame.display.flip()
            self.clock.tick(FRAME_RATE)

    def in_view(self, x, y):
        if 0 < x - self.camera['x'] - self.camera_window_x < self.camera['w']:
            if 0 < y - self.camera['y'] - self.camera_window_y < self.camera['h']:
                return True
        return False

    def draw_simulation_background(self):
        pygame.gfxdraw.filled_polygon(self.screen, [[self.camera_window_x, self.camera_window_y],
                                                    [self.camera_window_x + self.camera['w'], self.camera_window_y],
                                                    [self.camera_window_x + self.camera['w'],
                                                     self.camera_window_y + self.camera['h']],
                                                    [self.camera_window_x, self.camera_window_y + self.camera['h']]],
                                      SIMULATION_BACKGROUND)

    def draw_camera(self):
        pygame.draw.rect(self.screen, BLACK, (self.camera_window_x,
                                              self.camera_window_y,
                                              self.camera['w'], self.camera['h']),
                         int(self.width / 200))


if __name__ == '__main__':
    g = Graphics(Simulation(), 800, 600, 'Graphics test')
    g.run()
