import os
import PIL
import pygame

from myrpg.base_settings import *
from myrpg.file_loader import FilesLoader

class MyRPGPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, attack_func, destroy_weapon):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\player\\player_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -15)

        self.get_player_assets()

        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.10

        self.direction = pygame.math.Vector2()
        self.speed = 4

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_timer = 0
        self.attack_func = attack_func
        self.destroy_weapon = destroy_weapon

        self.weapon_index = 1
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.weapon_entry = WEAPON_DATA[list(WEAPON_DATA.keys())[self.weapon_index]]
        self.obstacle_sprites = obstacle_sprites

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
                print('magic!')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')        
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

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
                

        