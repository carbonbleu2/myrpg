import os
import random

import pygame

from myrpg.abilities.base_ability import BaseAbility
from myrpg.animation_manager import ParticleAnimationManager
from myrpg.base_settings import TILE_SIZE

class Fireball(BaseAbility):
    def __init__(self, animation_manager):
        super().__init__(animation_manager)
        self.name = 'Fireball'
        self.strength = 20
        self.cost = 15
        self.category = 'flame'
        self.codename = 'Fireball'
        self.description = "A small burst of fire, great for novice mages"

        self.damage_range = 3
        
        self.graphic = f"{os.path.join('graphics', 'abilities', self.category, self.codename)}.png"

        self.applicable_groups = ['visible', 'attack']

    def on_cast(self, player, groups, **kwargs):
        if player.energy >= self.cost:
            player.energy -= self.cost

            player_dir = player.status.split('_')[0]
            if player_dir == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player_dir == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player_dir == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, self.damage_range + 1):
                if direction.x:
                    offset_x = (direction.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_manager.create_ability_particles((x, y), 'Fireball', groups, player_dir)
                else:
                    offset_y = (direction.y * i) * TILE_SIZE
                    y = player.rect.centery + offset_y + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    x = player.rect.centerx + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_manager.create_ability_particles((x, y), 'Fireball', groups, player_dir)