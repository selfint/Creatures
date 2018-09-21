# main.py
# Description: main simulation.
# ---------------------------------------------------------------------------------------

# Imports
import pygame

# Constants
HEIGHT = 600
WIDTH = 800
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255


class Simulation:

    def __init__(self):
        pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Creatures')
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick()

