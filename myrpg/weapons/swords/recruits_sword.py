import os

import pygame

from myrpg.weapon import Weapon

class RecruitsSword(Weapon):
    name = "Recruit's Sword"
    cooldown = 100
    damage = 15
    category = "swords"
    codename = "RecruitsSword"
    graphic = os.path.join("graphics", "weapons", "swords", "RecruitsSword.png")
    pushback = 0.10
    description = "A basic blade for new adventurers, light yet reliable."
        
    def __init__(self, player, groups):
        super().__init__(player, groups)