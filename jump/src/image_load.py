"""File which mainly imports images"""
import os
from PIL import Image
import numpy as np
import pygame


# create check for if files exist
def import_folder(path):
    """Function which imports all of folder's images"""
    surface_list = []

    for _, __, img_file in os.walk(path):
        for image in img_file:
            full_path = path + '/' + image
            image_surf = pygame.image.load(check_path(full_path)).convert_alpha()
            if path == 'jump/assets/flowing_water':
                image_surf = pygame.transform.scale(image_surf, (20, 20))
            elif not image == 'charge.png':
                image_surf = pygame.transform.scale(image_surf, (36, 39))
            surface_list.append(image_surf)

    return surface_list


def check_path(path):
    """Checks if folder is present"""
    if not os.path.exists(path):
        print("path to needed folder does not exist, shutting program down")
        print("missing path: ", path)
        pygame.quit()
        exit()
    return path


def load_map(path):
    """Returns map in array form"""
    img = Image.open(check_path(path))
    level_map = np.array(img)
    return level_map


tile_size = 20
screen_height = 600
screen_width = 1200


