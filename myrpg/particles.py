import pygame

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, frames, *groups):
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = frames
        self.sprite_type = 'ability'
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center = position)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()