import os
import random
import math

import pygame

from myrpg.abilities.base_ability import BaseAbility
from myrpg.animation_manager import ParticleAnimationManager
from myrpg.base_settings import TILE_SIZE
from myrpg.timer import AbilityTimer

class WarriorsResolve(BaseAbility):
    def __init__(self, animation_manager):
        super().__init__(animation_manager)
        self.name = "Warrior's Resolve"
        self.strength = 20
        self.cost = 15
        self.category = 'warrior'
        self.codename = 'WarriorsResolve'
        self.description = "Steel your nerves to increase your defense by 30% for 5 seconds"

        self.damage_range = 3
        
        self.graphic = f"{os.path.join('graphics', 'abilities', self.category, self.codename)}.png"

        self.applicable_groups = ['visible', 'attack']

    def on_cast(self, player, groups, **kwargs):
        def end_of_ability(player, defense):
            # print("Old defense")
            player.defense = defense

        from myrpg.level import Level    
        if not self.codename in Level.timers or not Level.timers[self.codename].active:
            if player.energy >= self.cost:
                player.energy -= self.cost
            
            ability_duration = 5000
            old_player_defense = player.defense
            timer = AbilityTimer(ability_duration, end_of_ability, player, old_player_defense)
            Level.timers[self.codename] = timer
            Level.timers[self.codename].activate()
            player.defense = int(math.ceil(1.30 * player.defense))