import math
import os
import PIL
import pygame

from myrpg.abilities.ability_factory import AbilityFactory
from myrpg.base_settings import *
from myrpg.entity import Entity
from myrpg.file_loader import FilesLoader
from myrpg.weapons.weapon_factory import WeaponFactory

class MyRPGPlayer(Entity):
    def __init__(self, pos, groups, obstacle_sprites, attack_func, destroy_weapon, create_ability):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('graphics', 'player', 'player_down.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, 0)

        self.get_player_assets()

        self.status = 'down'
        
        self.obstacle_sprites = obstacle_sprites
        
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_timer = 0
        self.attack_func = attack_func
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = WeaponFactory.get_weapon_by_index(self.weapon_index)
        self.can_switch_weapons = True
        self.weapon_switch_time = None
        self.switch_cooldown = 500

        self.create_ability = create_ability
        self.ability_index = 0
        self.ability_entry = AbilityFactory.get_ability_by_index(self.ability_index)
        self.ability = self.ability_entry.name
        self.can_switch_abilities = True
        self.ability_switch_time = None
        
        self.stats = {
            'MaxHealth': 100,
            'MaxEnergy': 100,
            'Strength': 10,
            'Speed': 3,
            'Intelligence': 4
        }

        self.level = 1

        self.health = self.stats['MaxHealth']
        self.energy = self.stats['MaxEnergy']
        self.total_xp = 0
        self.xp_for_next_level = 15

        self.attack = int(math.ceil(0.8 * self.stats['Strength']))
        self.defense = int(math.ceil(0.2 * self.stats['Strength']))

        self.special_attack = int(math.ceil(0.8 * self.stats['Intelligence']))

        self.speed = self.stats['Speed']

        self.vulnerable = True
        self.hurt_time = 0
        self.invincibility_duration = 500

        self.health_recovery_rate = 0.001
        self.energy_recovery_rate = 0.005

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

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_player_assets(self):
        character_path = os.path.join('graphics', 'player')
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
                if self.ability_entry.damaging:
                    net_ability_damage = self.ability_entry.strength + self.stats['Intelligence']
                else:
                    net_ability_damage = 0
                self.create_ability(self.ability_entry, net_ability_damage, self.ability_entry.cost)

            if keys[pygame.K_a] and self.can_switch_weapons:
                self.can_switch_weapons = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= WeaponFactory.get_weapon_count():
                    self.weapon_index = 0
                self.weapon = WeaponFactory.get_weapon_by_index(self.weapon_index)
                
            if keys[pygame.K_s] and self.can_switch_abilities:
                self.can_switch_abilities = False
                self.ability_switch_time = pygame.time.get_ticks()
                self.ability_index += 1
                if self.ability_index >= AbilityFactory.get_ability_count():
                    self.ability_index = 0
                self.ability_entry = AbilityFactory.get_ability_by_index(self.ability_index)
                self.ability = self.ability_entry.name

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.recover_health()
        self.recover_energy()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_timer >= self.attack_cooldown + self.weapon.cooldown:
                self.attacking = False
                self.destroy_weapon()

        if not self.can_switch_weapons:
            if current_time - self.weapon_switch_time >= self.switch_cooldown:
                self.can_switch_weapons = True

        if not self.can_switch_abilities:
            if current_time - self.ability_switch_time >= self.switch_cooldown:
                self.can_switch_abilities = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_net_weapon_damage(self):
        return self.attack + self.weapon.damage
    
    def get_net_ability_damage(self):
        if not self.ability_entry.damaging:
            return 0
        return self.special_attack + self.ability_entry.strength
    
    def recover_energy(self):
        if self.energy < self.stats['MaxEnergy']:
            self.energy += self.energy_recovery_rate * self.stats['Intelligence']
        self.energy = min(self.energy, self.stats['MaxEnergy'])        

    def recover_health(self):
        if self.health < self.stats['MaxHealth']:
            self.health += self.health_recovery_rate * self.stats['Strength']
        self.health = min(self.health, self.stats['MaxHealth']) 

    def gain_xp(self, exp_gain):
        old_xp_for_level_gain = self.xp_for_next_level
        self.total_xp += exp_gain
        self.xp_for_next_level = self.xp_for_next_level - exp_gain
        while self.xp_for_next_level <= 0:
            self.level_up()
            self.xp_for_next_level = old_xp_for_level_gain + 15 + self.xp_for_next_level

    def level_up(self):
        self.level += 1
        self.stats['MaxHealth'] += 5
        self.stats['MaxEnergy'] += 3
        self.stats['Strength'] += 2
        self.stats['Intelligence'] += 2
        self.stats['Speed'] += 2
        