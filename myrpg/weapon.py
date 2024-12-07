import pygame

class Weapon(pygame.sprite.Sprite):
    name = None
    cooldown = None
    damage = None
    category = None
    codename = None
    graphic = None
    pushback = None

    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        player_dir = player.status.split('_')[0]
        
        weapon_graphic_path = f"graphics/weapons/{self.category}/animations/{self.codename}_{player_dir}.png"

        self.image = pygame.image.load(weapon_graphic_path).convert_alpha()

        if player_dir == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif player_dir == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif player_dir == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)

    def get_weapon_graphic_path(self, dir):
        return f"graphics/weapons/{self.category}/animations/{self.codename}_{dir}.png"