import random
import pygame

from myrpg.base_settings import TILE_SIZE, ENEMY_DATA
from myrpg.enemy import Enemy
from myrpg.file_loader import FilesLoader
from myrpg.tile import Tile
from myrpg.player import MyRPGPlayer
from myrpg.csv_utils import CSVUtils
from myrpg.ui import UI
from myrpg.weapon import Weapon

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

        self.ui = UI()

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
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                        if style == 'entity':
                            if col == '8':
                                self.player = MyRPGPlayer((736, 800), [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, self.destroy_weapon,
                                    self.create_ability)
                            elif col == '0':
                                Enemy('Blobble', (x, y), [self.visible_sprites], self.obstacle_sprites)
        
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_ability(self, name, strength, cost):
        print(f"{name}, {strength}, {cost}")

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


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
        