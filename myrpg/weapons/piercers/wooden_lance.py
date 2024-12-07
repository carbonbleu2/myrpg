import os

import pygame

from myrpg.weapon import Weapon

class WoodenLance(Weapon):
    name = "Wooden Lance"
    cooldown = 200
    damage = 18
    category = "piercers"
    codename = "WoodenLance"
    graphic = os.path.join("graphics", "weapons", "piercers", "WoodenLance.png")
    pushback = 0.50
        
    def __init__(self, player, groups):
        super().__init__(player, groups)