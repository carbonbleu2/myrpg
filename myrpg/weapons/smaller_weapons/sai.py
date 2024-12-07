import os

import pygame

from myrpg.weapon import Weapon

class Sai(Weapon):
    name = "Sai"
    cooldown = 50
    damage = 8
    category = "smaller_weapons"
    codename = "Sai"
    graphic = os.path.join("graphics", "weapons", "smaller_weapons", "Sai.png")
    pushback = 0.20
        
    def __init__(self, player, groups):
        super().__init__(player, groups)