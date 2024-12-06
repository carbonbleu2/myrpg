import os

from myrpg.abilities.base_ability import BaseAbility
from myrpg.animation_manager import ParticleAnimationManager

class Fireball(BaseAbility):
    def __init__(self, animation_manager):
        super().__init__(animation_manager)
        self.name = 'Fireball'
        self.strength = 5
        self.cost = 15
        self.category = 'flame'
        self.codename = 'Fireball'
        
        self.graphic = f"{os.path.join('graphics', 'abilities', self.category, self.codename)}.png"

        self.applicable_groups = ['visible', 'attack']

    def on_cast(self, player, groups, **kwargs):
        pass