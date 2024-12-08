import os
import re

import pygame

class FilesLoader:
    @staticmethod
    def import_images(path):
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text) ]

        surfaces = []
        for _, _, image_files in os.walk(path):
            image_files = sorted(image_files, key=natural_keys)
            for image in image_files:
                image_path = os.path.join(path, image)
                image_surface = pygame.image.load(image_path).convert_alpha()
                surfaces.append(image_surface)

        return surfaces