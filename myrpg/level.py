import random
import pygame

from myrpg.base_settings import TILE_SIZE
from myrpg.file_loader import FilesLoader
from myrpg.tile import Tile
from myrpg.player import MyRPGPlayer
from myrpg.csv_utils import CSVUtils
from myrpg.weapon import Weapon

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None


        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': CSVUtils.import_map('maps\\Map1._FloorBlocks.csv'),
            'grass': CSVUtils.import_map('maps\\Map1._Grass.csv'),
            'object': CSVUtils.import_map('maps\\Map1._Objects.csv'),
        }

        graphics = {
            'grass': FilesLoader.import_images('graphics\\grass'),
            'objects': FilesLoader.import_images('graphics\\objects')
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
        #         if col == 'r':
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = MyRPGPlayer((x, y), [self.visible_sprites], self.obstacle_sprites)
        self.player = MyRPGPlayer((736, 800), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_weapon)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

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
        