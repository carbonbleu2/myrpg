import os

import pygame

from myrpg.weapon import Weapon

class BloodSword(Weapon):
    name = "Blood Sword"
    cooldown = 100
    damage = 30
    category = "swords"
    codename = "BloodSword"
    graphic = os.path.join("graphics", "weapons", "swords", "BloodSword.png")
    pushback = 0.80
    description = "Dark blade that drains life when damaging foes."
        
    def __init__(self, player, groups):
        super().__init__(player, groups)

    @staticmethod
    def on_hit(player, damage):
        player.health += 0.15 * damage