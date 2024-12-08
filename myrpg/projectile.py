import pygame

from myrpg.particles import ParticleEffect

class Projectile(ParticleEffect):
    def __init__(self, position, frames, velocity, groups, range_):
        super().__init__(position, frames, groups)
        self.velocity = velocity
        self.range = range_
        self.init_position = position

    def update(self):
        super(Projectile, self).update()
        start_pos = self.init_position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.range is not None:
            current_pos = pygame.math.Vector2(self.rect.center)
            dist = (current_pos - start_pos).magnitude()
            print(start_pos, current_pos, dist)
            if dist >= self.range:
                self.kill()
