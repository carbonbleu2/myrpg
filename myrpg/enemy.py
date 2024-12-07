import os

import pygame

from myrpg.entity import Entity
from myrpg.base_settings import *
from myrpg.file_loader import FilesLoader

class Enemy(Entity):
    def __init__(self, name, position, groups, obstacle_sprites, damage_player, trigger_death_particles):
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

        self.can_attack = True
        self.attack_cooldown = 1000
        self.attack_timer = 0

        self.hit_time = 0
        self.vulnerable = True
        self.invincibility_duration = 300

        self.damage_player = damage_player

        self.trigger_death_particles = trigger_death_particles

        self.temp_stats = {
            'pushback': 0
        }

    def import_graphics(self, name):
        self.animations = {
            'idle': [],
            'move': [],
            'attack': []
        }

        path = os.path.join('graphics', 'enemy_anim', name)
        for animation in self.animations.keys():
            self.animations[animation] = FilesLoader.import_images(os.path.join(path, animation))

    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        dist, _ = self.get_player_distance_and_direction(player)

        if dist <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif dist <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def update(self):
        self.on_hit()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def actions(self, player):
        if self.status == 'attack':
            self.attack_timer = pygame.time.get_ticks()
            self.damage_player(self.damage, self.attack_type)
        elif self.status == 'move':
            _, self.direction = self.get_player_distance_and_direction(player)
        else:
            self.direction = pygame.math.Vector2()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        if self.health <= 0:
            player.gain_xp(self.exp_gain)
            
        self.on_death()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_timer >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, damage_source):
        if self.vulnerable:
            _, self.direction = self.get_player_distance_and_direction(player)
            if damage_source == 'weapon':
                self.health -= player.get_net_weapon_damage()
                self.temp_stats['pushback'] = player.weapon.pushback
            else:
                self.health -= player.get_net_ability_damage()
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def on_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.name)

    def on_hit(self):
        if not self.vulnerable:
            self.direction *= -self.temp_stats['pushback']