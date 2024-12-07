import random
import pygame

from myrpg.animation_manager import ParticleAnimationManager
from myrpg.abilities.ability_factory import AbilityFactory
from myrpg.base_settings import TILE_SIZE, ENEMY_ID
from myrpg.enemy import Enemy
from myrpg.file_loader import FilesLoader
from myrpg.tile import Tile
from myrpg.player import MyRPGPlayer
from myrpg.csv_utils import CSVUtils
from myrpg.ui import UI
from myrpg.weapon import Weapon

class Level:
    timers = {}

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

        self.ui = UI()

        self.animation_manager = ParticleAnimationManager()
        AbilityFactory.set_animation_manager(self.animation_manager)

    def create_map(self):
        layouts = {
            'boundary': CSVUtils.import_map('maps\\Map1._FloorBlocks.csv'),
            'grass': CSVUtils.import_map('maps\\Map1._Grass.csv'),
            'object': CSVUtils.import_map('maps\\Map1._Objects.csv'),
            'entity': CSVUtils.import_map('maps\\Map1._Entities.csv')
        }

        graphics = {
            'grass': FilesLoader.import_images('graphics\\grass'),
            'objects': FilesLoader.import_images('graphics\\objects'),
            'entities': FilesLoader.import_images('graphics\\enemies')
        }

        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != '-1':
                        x = j * TILE_SIZE
                        y = i * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass = random.choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                'grass', random_grass)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                        if style == 'entity':
                            if col == '8':
                                self.player = MyRPGPlayer((736, 800), [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, self.destroy_weapon,
                                    self.create_ability)
                            else:
                                Enemy(ENEMY_ID[int(col)], (x, y), [self.visible_sprites, self.attackable_sprites], 
                                      self.obstacle_sprites, self.damage_player, self.trigger_death_particles)
        
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.update_enemy(self.player)
        self.player_attack()
        self.ui.display(self.player)
        for k, v in list(self.timers.items()):
            v.update()
            if not v.active:
                del self.timers[k]

    def create_attack(self):
        self.current_attack = self.player.weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_ability(self, ability, strength=None, cost=None):
        if strength is None:
            strength = ability.strength
        if cost is None:
            cost = ability.cost

        groups = []
        for group_name in ability.applicable_groups:
            if group_name == 'visible':
                groups.append(self.visible_sprites)
            elif group_name == 'attack':
                groups.append(self.attack_sprites)

        ability.on_cast(self.player, groups)

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target in collision_sprites:
                        if target.sprite_type == 'grass':
                            position = target.rect.center
                            self.animation_manager.create_particles(position, 'Bump', [self.visible_sprites])
                            target.kill()
                        else:
                            target.get_damage(self.player, attack_sprite.sprite_type)
                            

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            amount -= self.player.defense
            self.player.health = 0 if self.player.health - amount <= 0 else self.player.health - amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_manager.create_particles(self.player.rect.center, attack_type, [self.visible_sprites])

    def trigger_death_particles(self, position, enemy_name):
        self.animation_manager.create_enemy_death_particles(position, enemy_name, self.visible_sprites)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.half_width = self.surface.get_size()[0] // 2
        self.half_height = self.surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor = pygame.image.load('maps\\Map1.png').convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset = self.floor_rect.topleft - self.offset
        self.surface.blit(self.floor, floor_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_rect)

    def update_enemy(self, player):
        enemy_sprites: list[Enemy] = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

        
        