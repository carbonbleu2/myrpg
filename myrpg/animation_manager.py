import os

import pygame

from myrpg.file_loader import FilesLoader
from myrpg.particles import ParticleEffect

class ParticleAnimationManager:
    def __init__(self):
        self.frames = {
            'Slash': None,
            'Bump': None,
            'EnemyDeath': {
                'Blobble': None
            },
            'Ability': {
                'Fireball': {
                    'left': None,
                    'right': None,
                    'up': None,
                    'down': None
                },
                'FirstAid': None
            }
        }

        for key in self.frames:
            if key not in ['EnemyDeath', 'Ability']:
                self.frames[key] = FilesLoader.import_images(os.path.join('graphics', 'particles', key))
            for key in self.frames['EnemyDeath']:
                self.frames['EnemyDeath'][key] = FilesLoader.import_images(os.path.join('graphics', 'particles', 'EnemyDeath', key))
            for key in self.frames['Ability']:
                if isinstance(self.frames['Ability'][key], dict):
                    for dir in self.frames['Ability'][key]:
                        self.frames['Ability'][key][dir] = FilesLoader.import_images(os.path.join('graphics', 'particles', 'Abilities', key, dir))
                else:
                    self.frames['Ability'][key] = FilesLoader.import_images(os.path.join('graphics', 'particles', 'Abilities', key))

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_particles(self, position, particle_name, groups):
        frames = self.frames[particle_name]
        ParticleEffect(position, frames, groups)

    def create_enemy_death_particles(self, position, enemy_name, groups):
        frames = self.frames['EnemyDeath'][enemy_name]
        ParticleEffect(position, frames, groups)

    def create_ability_particles(self, position, ability_name, groups, direction=None):
        if direction:
            frames = self.frames['Ability'][ability_name][direction]
        else:
            frames = self.frames['Ability'][ability_name]
        ParticleEffect(position, frames, groups)