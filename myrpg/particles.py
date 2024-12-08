import pygame

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, frames, *groups, 
                cycle=False, 
                stick_to_player=False, 
                player=None):
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = frames
        self.sprite_type = 'ability'
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center = position)
        self.cycle = cycle
        self.stick_to_player = stick_to_player
        self.player = player

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            if self.cycle:
                self.frame_index = 0
                self.image = self.frames[int(self.frame_index)]
            else:
                self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
        if self.stick_to_player and self.player:
            self.rect.center = self.player.rect.center

    def update(self):
        self.animate()