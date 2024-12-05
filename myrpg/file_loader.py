import os

import pygame

class FilesLoader:
    @staticmethod
    def import_images(path):
        # if path == 'graphics\\enemies':
        #     import pdb
        #     pdb.set_trace()
        surfaces = []
        for _, _, image_files in os.walk(path):
            for image in image_files:
                image_path = os.path.join(path, image)
                image_surface = pygame.image.load(image_path).convert_alpha()
                surfaces.append(image_surface)

        return surfaces