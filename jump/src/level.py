"""file containing the class level"""

import time
import pygame
from src.tiles import Tile, Slopes, Princess
from src.player import Player
from src.image_load import *
from src.colors import *


class Level:
    """Class containing all the map's information"""
    def __init__(self, level_data, surface):

        # map setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

        self.background = pygame.image.load(check_path('jump/assets/pixel_cavern_background.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background, (1200, 600))
        self.background_height = -1000

        # time
        self.time_font = pygame.font.Font(None, 22)
        self.start_time = time.time()
        self.last_time = self.start_time
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def setup_level(self, layout):
        """sets up the level"""
        self.tiles = pygame.sprite.Group()
        self.slopes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.princess = pygame.sprite.GroupSingle()

        stone_image = pygame.image.load(check_path('jump/assets/blocks/stone.png')).convert_alpha()
        stone_image = pygame.transform.scale(stone_image, (tile_size, tile_size))
        ice_image = pygame.image.load(check_path('jump/assets/Custom_ice.png')).convert_alpha()
        princess_image = pygame.image.load(check_path('jump/assets/princess.png')).convert_alpha()
        princess_image = pygame.transform.scale(princess_image, (36, 45))

        for row_index, row in enumerate(layout):
            for col_index, pixel in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if np.array_equal(red, pixel) or np.array_equal(red_alpha, pixel):
                    tile = Tile((x, y), stone_image)
                    self.tiles.add(tile)
                elif np.array_equal(green, pixel) or np.array_equal(green_alpha, pixel):
                    slope = Slopes((x, y), 'left')
                    self.slopes.add(slope)
                elif np.array_equal(pink, pixel) or np.array_equal(pink_alpha, pixel):
                    slope = Slopes((x, y), 'right')
                    self.slopes.add(slope)
                elif np.array_equal(player_tile, pixel) or np.array_equal(player_tile_alpha, pixel):
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif np.array_equal(blue, pixel) or np.array_equal(blue_alpha, pixel):
                    tile = Tile((x, y), ice_image, 0.3)
                    self.tiles.add(tile)
                elif np.array_equal(orange, pixel) or np.array_equal(orange_alpha, pixel):
                    princess = Princess((x, y), princess_image)
                    self.princess.add(princess)

    def run(self, jump_trigger, charge, screen):
        """runs the whole game,
        generates all tiles,
        checks collisions and updates the player's position
        """

        # level tiles
        screen.blit(self.background, (0, 0))

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.slopes.update(self.world_shift)
        self.slopes.draw(self.display_surface)
        self.princess.update(self.world_shift)
        self.princess.draw(self.display_surface)

        # collision
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.slope_collision()

        # player
        self.player.update(jump_trigger, charge)
        self.player.draw(self.display_surface)
        self.next_screen()

        # end state screen
        self.princess_collision(screen)
        self.display_time(screen)

    def horizontal_movement_collision(self):
        """checks horizontal collisions"""

        player = self.player.sprite
        player.apply_movement()

        if player.rect.right > screen_width:
            player.rect.right = screen_width
            player.direction.x = -1

        if player.rect.left < 0:
            player.rect.left = 0
            player.direction.x = 1

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 or (player.last_direction.x < 0 and player.movement_speed != 0):
                    player.direction.x = 1
                    player.movement_speed *= -1
                    player.last_direction.x = 1
                    player.speed -= 2
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0 or (player.last_direction.x > 0 and player.movement_speed != 0):
                    player.last_direction.x = -1
                    player.movement_speed *= -1
                    player.direction.x = -1
                    player.speed -= 2
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        """checks vertical collisions"""
        player = self.player.sprite

        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # on top of the block
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.in_air = False
                    player.direction.y = 0
                    player.friction = sprite.friction
                # bellow the block
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 3

    def next_screen(self):
        """function that moves the screen up when character crosses the upper border of the screen"""
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < 0 and direction_y < 0:
            self.world_shift += screen_height
            player.rect.centery += screen_height
        elif player_y > screen_height and direction_y > 0:
            self.world_shift -= screen_height
            player.rect.centery -= screen_height
        else:
            self.world_shift = 0

    def debug_teleport(self):
        """debug teleport up, can teleport out of the map"""
        self.world_shift += screen_height

    def slope_collision(self):
        """checks slope collisions"""
        player = self.player.sprite

        for slope in self.slopes.sprites():
            if slope.rect.colliderect(player.rect):
                if slope.direction == 'left':
                    player.direction.x = -1
                    player.rect.bottomright = slope.rect.midleft
                    player.direction.y = +2

                elif slope.direction == 'right':
                    player.direction.x = 1
                    player.rect.bottomleft = slope.rect.midright
                    player.direction.y = +2

    def princess_collision(self, screen):
        """checks for collision with the princess sprite"""
        player = self.player.sprite

        text_font = pygame.font.Font(None, 200)
        text_font2 = pygame.font.Font(None, 100)
        text_font3 = pygame.font.Font(None, 50)
        text_surface = text_font.render('You win', False, "Black")
        time_text = "Your time: " + str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds)
        text_surface2 = text_font2.render(time_text, False, "Black")
        text_surface3 = text_font3.render('Press any key to close the game', False, "Black")

        rect_text = text_surface.get_rect(midbottom=(screen_width / 2, screen_height / 2))
        rect_text2 = text_surface2.get_rect(midtop=(screen_width / 2, screen_height / 2))
        rect_text3 = text_surface3.get_rect(midtop=rect_text2.midbottom)

        for sprite in self.princess.sprites():
            if sprite.rect.colliderect(player.rect):

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                            pygame.quit()
                            exit()
                    screen.blit(text_surface, rect_text)
                    screen.blit(text_surface2, rect_text2)
                    screen.blit(text_surface3, rect_text3)
                    pygame.display.update()

    def display_time(self, screen):
        """displays time elapsed"""
        self.last_time = time.time()

        total_seconds = int(self.last_time - self.start_time)
        self.hours = int(total_seconds / 3600)
        self.minutes = int(total_seconds / 60) % 60
        self.seconds = total_seconds % 60

        time_text = "TIME: " + str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds)
        text_surface = self.time_font.render(time_text, False, "white")
        rect1 = text_surface.get_rect(topright=(1200, 0))

        screen.blit(text_surface, rect1)
