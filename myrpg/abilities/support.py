import os
from myrpg.abilities.base_ability import BaseAbility

class FirstAid(BaseAbility):
    def __init__(self, animation_manager):
        super().__init__(animation_manager)
        self.name = 'First Aid'
        self.strength = 20
        self.cost = 10
        self.category = 'support'
        self.codename = 'FirstAid'
        
        self.damage_range = 0

        self.graphic = f"{os.path.join('graphics', 'abilities', self.category, self.codename)}.png"
        
        self.applicable_groups = ['visible']

    def on_cast(self, player, groups, **kwargs):
        super(FirstAid, self).on_cast(player, groups, **kwargs)
        if player.energy >= self.cost and player.health < player.stats['MaxHealth']:
            player.health += self.strength
            player.energy -= self.cost
            if player.health >= player.stats['MaxHealth']:
                player.health = player.stats['MaxHealth']
            self.animation_manager.create_ability_particles(player.rect.center, self.codename, groups)