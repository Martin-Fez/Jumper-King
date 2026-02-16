from sys import exit
import pygame
from src.level import Level
from src.image_load import screen_width, screen_height, load_map, check_path

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jump-er king')
icon = pygame.image.load(check_path('jump/assets/icon.png')).convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
level = Level(load_map("jump/assets/map/game_map.png"), screen)
charge = 0
jump = 0

title_font = pygame.font.Font(None, 200)
subtitle_font = pygame.font.Font(None, 100)
text_surface = title_font.render('Jump-er king', False, "Black")
text_surface2 = subtitle_font.render('Press any key to start', False, "Black")
background = pygame.image.load(check_path('jump/assets/pixel_cavern_background.png')).convert_alpha()
background = pygame.transform.scale(background, (1200, 600))
rect_text = text_surface.get_rect(midbottom=(screen_width / 2, screen_height / 2))
rect_text2 = text_surface2.get_rect(midtop=(screen_width / 2, screen_height / 2))

intro_screen = True
while intro_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            intro_screen = False
            break

    screen.blit(background, (0, 0))
    screen.blit(text_surface, rect_text)
    screen.blit(text_surface2, rect_text2)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                charge = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                charge = 0
                jump = 1

            # if trigger debug function
            if event.key == pygame.K_n:
                level.debug_teleport()

    level.run(jump, charge, screen)
    jump = 0

    pygame.display.update()
    screen.fill('black')
    clock.tick(60)
