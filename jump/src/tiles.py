"""File containing all the non-player sprites"""
import pygame
from src.image_load import import_folder, check_path


class Tile(pygame.sprite.Sprite):
    """Class for standart tiles"""
    def __init__(self, pos, image, friction=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.friction = friction

    def update(self, y_shift):
        """updates tile's position"""
        self.rect.y += y_shift


class Slopes(pygame.sprite.Sprite):
    """Class for 'slope' tiles also known as flowing water tiles"""
    def __init__(self, pos, direction):
        super().__init__()
        self.direction = direction

        self.import_tile_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['flowing_water'][int(self.frame_index)]

        self.rect = self.image.get_rect(topleft=pos)

    def import_tile_assets(self):
        """Function which imports tile's animation assets"""
        character_path = 'jump/assets/'
        self.animations = {'flowing_water': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(check_path(full_path))

    def animate(self):
        """Function which animates the tile"""
        animation = self.animations['flowing_water']

        # looping frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.direction == 'right':
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def update(self, y_shift):
        """Function that calls the animation and updates the tile's position"""
        self.animate()
        self.rect.y += y_shift


class Princess(pygame.sprite.Sprite):
    """Class for the 'princess' tile, a tile which upon collision ends the game"""
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y -= 25

    def update(self, y_shift):
        """updates tile's position"""
        self.rect.y += y_shift
