# graphics.py
# Description: graphic representation of the simulation. Camera is drawn from top left corner.
# ---------------------------------------------------------------------------------------------------------------------

# Imports
from typing import Union

# Pygame
import pygame
from pygame import gfxdraw

# Constants
from Constants.constants import BACKGROUND, BLACK, CAMERA_SPEED, CAPTION, CENTER, FRAME_RATE, GREY, \
    SIMULATION_BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH, TEXT_ONLY
from Constants.types import COLOR
# Objects
from creature import Creature
from functions import ignore
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

    def __init__(self, simulation: Simulation, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT, caption: str = CAPTION):
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
                       'w': self.width / 1.5, 'h': self.height / 1.5}

    def run(self) -> None:
        text = TEXT_ONLY
        while True:
            print("Running in textual mode.")
            for epoch in range(self.simulation.generation_time):
                self.simulation.update(text)

    def text_run(self) -> None:
        while True:
            self.simulation.update()

    def graphical_run(self) -> None:
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
                        self.camera_dx = -CAMERA_SPEED
                    if event.key == pygame.K_UP:
                        self.camera_dy = -CAMERA_SPEED
                    if event.key == pygame.K_RIGHT:
                        self.camera_dx = CAMERA_SPEED
                    if event.key == pygame.K_DOWN:
                        self.camera_dy = CAMERA_SPEED

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.camera_dx = 0
                    if event.key == pygame.K_UP:
                        self.camera_dy = 0
                    if event.key == pygame.K_RIGHT:
                        self.camera_dx = 0
                    if event.key == pygame.K_DOWN:
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

            self.draw_borders()

            self.draw_camera()

            # Update frame.
            pygame.display.flip()
            self.clock.tick(FRAME_RATE)

    def draw_borders(self) -> None:
        """
        Draw the outline of the world, if it is in view of the camera.
        """
        # Draw world outline (if in view of camera).
        world = [(self.camera_window_x, self.camera_window_y),
                 (self.simulation.world_width, self.camera_window_y),
                 (self.camera_window_x, self.simulation.world_height),
                 (self.simulation.world_width, self.simulation.world_height)]

        # Check if one of the world corners is in view of the camera.
        drawn = False
        for sx, sy in world:
            if self.in_view(sx, sy):

                # Check if another one of the corners is in view of the camera.
                # If it is, draw a line to it, unless they are opposite corners then don't.
                for ex, ey in ignore(world, (sx, sy)):
                    if self.in_view(ex, ey) and ((sx + ex) != self.simulation.world_width
                                                 or (sy + ey != self.simulation.world_height)):
                        pygame.draw.aaline(self.screen, BLACK,
                                           (sx - self.camera['x'], sy - self.camera['y']),
                                           (ex - self.camera['x'], ey - self.camera['y']))
                        drawn = True

                    # If no other corners were in view, draw lines to edges of the camera view.
                    else:
                        source_x = sx - self.camera['x']
                        source_y = sy - self.camera['y']

                        corner_x = ex - self.camera['x']
                        actual_x = max(corner_x, self.camera_window_x) if corner_x < self.camera_window_x \
                            else min(corner_x, self.camera_window_x + self.camera['w'])
                        corner_y = ey - self.camera['y']
                        actual_y = max(corner_y, self.camera_window_y) if corner_y < self.camera_window_y \
                            else min(corner_y, self.camera_window_y + self.camera['h'])

                        # Don't connect opposite corners.
                        if not (world.index((sx, sy)) + world.index((ex, ey)) == 3):
                            pygame.draw.aaline(self.screen, BLACK,
                                               (source_x, source_y),
                                               (actual_x, actual_y))
                            drawn = True

        # Check if no corners are in view, but an edge is.
        if not drawn:

            # Left edge.
            if self.in_view(x=self.camera_window_x):
                pygame.draw.line(self.screen, BLACK, (self.camera_window_x - self.camera['x'], self.camera_window_y),
                                 (self.camera_window_x - self.camera['x'], self.camera_window_y + self.camera['h']))

            # Right edge.
            if self.in_view(x=self.camera_window_x + self.camera['w']):
                pygame.draw.line(self.screen, BLACK, (self.camera_window_x - self.camera['x'] + self.camera['w'], self.camera_window_y),
                                 (self.camera_window_x - self.camera['x'] + self.camera['w'], self.camera_window_y + self.camera['h']))

    def in_view(self, x: int = None, y: int = None) -> bool:
        """
        Checks if an object is in view of the camera.
        """
        if x is None or (0 <= x - self.camera['x'] - self.camera_window_x <= self.camera['w']):
            if y is None or (0 <= y - self.camera['y'] - self.camera_window_y <= self.camera['h']):
                return True
        return False

    def draw_simulation_background(self):
        """
        Draws the background for the simulation.
        """
        pygame.gfxdraw.filled_polygon(self.screen, [[self.camera_window_x, self.camera_window_y],
                                                    [self.camera_window_x + self.camera['w'], self.camera_window_y],
                                                    [self.camera_window_x + self.camera['w'],
                                                     self.camera_window_y + self.camera['h']],
                                                    [self.camera_window_x, self.camera_window_y + self.camera['h']]],
                                      SIMULATION_BACKGROUND)

    def draw_camera(self):
        """
        Draws the borders of the camera window.
        """
        pygame.draw.rect(self.screen, BLACK, (self.camera_window_x,
                                              self.camera_window_y,
                                              self.camera['w'], self.camera['h']),
                         int(self.width / 200))

    def opposite(self, corner_a: tuple, corner_b: tuple, world: list) -> bool:
        """
        Returns True if the corners are opposite.
        """
        return world.index(corner_a) + world.index(corner_b) == 3


if __name__ == '__main__':
    g = Graphics(Simulation(), 800, 600, 'Graphics test')
    g.graphical_run()
