import os

import pygame

from myrpg.entity import Entity
from myrpg.base_settings import *
from myrpg.file_loader import FilesLoader

class Enemy(Entity):
    def __init__(self, name, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.import_graphics(name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        self.name = name
        data = ENEMY_DATA[self.name]

        self.health = data['MaxHealth']
        self.exp_gain = data['ExpGain']
        self.damage = data['Damage']
        self.attack_type = data['AttackType']
        self.speed = data['Speed']
        self.resistance = data['Resistance']
        self.attack_radius = data['AttackRadius']
        self.notice_radius = data['NoticeRadius']

    def import_graphics(self, name):
        character_path = 'graphics\\enemy_anim'
        self.animations = {
            'idle': [],
            # 'move': [],
            # 'attack': []
        }

        path = f"graphics\\enemy_anim\\{name}"
        for animation in self.animations.keys():
            self.animations[animation] = FilesLoader.import_images(os.path.join(path, animation))

    def update(self):
        self.move(self.speed)