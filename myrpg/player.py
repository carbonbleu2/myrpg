import os
import PIL
import pygame

from myrpg.base_settings import *
from myrpg.entity import Entity
from myrpg.file_loader import FilesLoader

class MyRPGPlayer(Entity):
    def __init__(self, pos, groups, obstacle_sprites, attack_func, destroy_weapon, create_ability):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\player\\player_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -15)

        self.get_player_assets()

        self.status = 'down'
        
        self.obstacle_sprites = obstacle_sprites
        
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_timer = 0
        self.attack_func = attack_func
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.weapon_entry = WEAPON_DATA[list(WEAPON_DATA.keys())[self.weapon_index]]
        self.can_switch_weapons = True
        self.weapon_switch_time = None
        self.switch_cooldown = 200

        self.create_ability = create_ability
        self.ability_index = 0
        self.ability = list(ABILITY_DATA.keys())[self.ability_index]
        self.ability_entry = ABILITY_DATA[list(ABILITY_DATA.keys())[self.ability_index]]
        self.can_switch_abilities = True
        self.ability_switch_time = None
        
        self.stats = {
            'MaxHealth': 100,
            'MaxEnergy': 100,
            'Attack': 10,
            'Magic': 4,
            'Speed': 3 
        }

        self.health = self.stats['MaxHealth']
        self.energy = self.stats['MaxEnergy']
        self.xp = 123
        self.speed = self.stats['Speed']

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_player_assets(self):
        character_path = 'graphics\\player'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': []
        }

        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = FilesLoader.import_images(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_z]:
                self.attacking = True
                self.attack_timer = pygame.time.get_ticks()
                self.attack_func()

            if keys[pygame.K_x]:
                self.attacking = True
                self.attack_timer = pygame.time.get_ticks()
                net_ability_damage = self.ability_entry['Strength'] + self.stats['Magic']
                self.create_ability(self.ability_entry['Name'], net_ability_damage, self.ability_entry['Cost'])

            if keys[pygame.K_a] and self.can_switch_weapons:
                self.can_switch_weapons = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(WEAPON_DATA.keys()):
                    self.weapon_index = 0
                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
                self.weapon_entry = WEAPON_DATA[list(WEAPON_DATA.keys())[self.weapon_index]]

            if keys[pygame.K_s] and self.can_switch_abilities:
                self.can_switch_abilities = False
                self.ability_switch_time = pygame.time.get_ticks()
                self.ability_index += 1
                if self.ability_index >= len(ABILITY_DATA.keys()):
                    self.ability_index = 0
                self.ability = list(ABILITY_DATA.keys())[self.ability_index]
                self.ability_entry = ABILITY_DATA[list(ABILITY_DATA.keys())[self.ability_index]]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_timer >= self.attack_cooldown:
                self.attacking = False
                self.destroy_weapon()

        if not self.can_switch_weapons:
            if current_time - self.weapon_switch_time >= self.switch_cooldown:
                self.can_switch_weapons = True

        if not self.can_switch_abilities:
            if current_time - self.ability_switch_time >= self.switch_cooldown:
                self.can_switch_abilities = True
                

        