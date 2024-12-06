import pygame

from myrpg.player import MyRPGPlayer

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: MyRPGPlayer, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        player_dir = player.status.split('_')[0]
        
        player_weapon = player.weapon_entry
        player_weapon_name = player.weapon

        weapon_graphic_path = f"graphics/weapons/{player_weapon['Category']}/animations/{player_weapon_name}_{player_dir}.png"

        self.image = pygame.image.load(weapon_graphic_path).convert_alpha()

        if player_dir == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif player_dir == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif player_dir == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)