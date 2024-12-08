import os
import random

import pygame

from myrpg.abilities.base_ability import BaseAbility
from myrpg.animation_manager import ParticleAnimationManager
from myrpg.base_settings import TILE_SIZE

class FrostAbility(BaseAbility):
    def __init__(self, animation_manager):
        super().__init__(animation_manager)
        self.name = 'Frost'
        self.strength = 18
        self.cost = 15
        self.category = 'ice'
        self.codename = 'Frost'
        self.damaging = True
        self.description = "A small, quick burst of ice"

        self.damage_range = 100
        
        self.graphic = f"{os.path.join('graphics', 'abilities', self.category, self.codename)}.png"

        self.applicable_groups = ['visible', 'attack']

        self.proj_velocity = 20

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
            projectile = self.animation_manager.create_projectile(player.rect.center, 'Fireball', self.proj_velocity, groups, player_dir, self.damage_range)