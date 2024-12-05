import sys

import pygame

from myrpg.base_settings import *
from myrpg.level import Level

class MyRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("MyRPG")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("grey")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)