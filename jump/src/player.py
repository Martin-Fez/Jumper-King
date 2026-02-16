"""File containing the class Player"""
import pygame
from src.image_load import import_folder, check_path


class Player(pygame.sprite.Sprite):
    """Class containing all the functions for the player sprite"""
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.status = 'idle'
        self.facing_right = True

        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.movement_speed = 0
        self.friction = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.last_direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = 0
        self.speed = 8
        self.in_air = False

    def player_input(self, jump_trigger):
        """Function which reads the player's inputs"""
        keys = pygame.key.get_pressed()

        if jump_trigger and not self.in_air:
            self.jump()
            self.in_air = True
            self.friction = 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.last_direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.last_direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

    def apply_gravity(self):
        """Function that applies gravity upon the player sprite"""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.direction.y > 2 * self.gravity:
            self.friction = 0
            self.in_air = True

        # cap on falling speed
        if self.direction.y > 30 * self.gravity:
            self.direction.y = 30 * self.gravity

    def apply_friction(self):
        """Function that simulates friction with the ground the player's standing on"""
        if self.friction <= 0:
            self.movement_speed = 0
            return

        if self.movement_speed != 0:
            if self.movement_speed > 0:
                self.movement_speed -= self.friction
                if self.movement_speed < 0:
                    self.movement_speed = 0
            else:
                self.movement_speed += self.friction
                if self.movement_speed > 0:
                    self.movement_speed = 0

    def jump(self):
        """Function which makes the player jump"""
        self.friction = 0
        self.speed = 8
        self.direction.y = self.jump_speed
        self.jump_speed = 0

    def apply_movement(self):
        """Function which applies the player's movement in the x direction"""
        if not self.in_air:
            self.speed = 4

        self.movement_speed += self.direction.x * self.speed
        if self.movement_speed > self.speed:
            self.movement_speed = self.speed

        if self.movement_speed < -self.speed:
            self.movement_speed = -self.speed

        self.rect.x += self.movement_speed

        self.apply_friction()

    def charge_jump(self):
        """Function which charge's the player's jump"""
        self.jump_speed -= 0.5
        self.direction.x = 0

        if self.jump_speed < -20:
            self.jump_speed = -20

    def import_character_assets(self):
        """Function which imports the character's animation assets"""
        character_path = 'jump/assets/jump_king_sprite/'
        self.animations = {'idle': [], 'walk': [], 'jump': [], 'charge': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(check_path(full_path))

    def get_status(self, charge):
        """Function which gets the player's animation status"""

        if charge and not self.in_air:
            self.status = 'charge'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.in_air:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'walk'
        else:
            self.status = 'idle'

    def animate(self):
        """Function which animates the player"""
        animation = self.animations[self.status]

        # looping frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        if not self.in_air:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, jump_trigger, charge):
        """Function which changes player's position, animation sprite and status"""
        self.get_status(charge)
        self.animate()
        if charge and not self.in_air:
            self.charge_jump()
            return
        if not self.in_air:
            self.player_input(jump_trigger)
