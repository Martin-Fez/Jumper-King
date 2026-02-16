import os

import numpy as np
import pytest
from src.image_load import check_path, load_map
from src.tiles import Slopes
from src.level import Level
from src.player import Player
import pygame


@pytest.mark.parametrize(
    'path, expected',
    [
        ('jump/assets/flowing_water', 'jump/assets/flowing_water'),
        ('jump/assets/pixel_cavern_background.png', 'jump/assets/pixel_cavern_background.png'),
        ('jump/assets/icon.png', 'jump/assets/icon.png'),
    ])
def test_check_path(path, expected):
    assert expected == check_path(path)


def test_player_jump():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    x = 0
    y = 0
    player = pygame.sprite.GroupSingle()
    player_sprite = Player((x, y))
    player.add(player_sprite)
    player.sprite.jump_speed = -5
    player.sprite.update(True, False)
    assert player.sprite.direction.y == -5


def test_player_jump_animation():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    x = 0
    y = 0
    player = pygame.sprite.GroupSingle()
    player_sprite = Player((x, y))
    player.add(player_sprite)
    player.sprite.jump_speed = -5
    player.sprite.update(True, False)
    player.sprite.update(True, False)
    assert player.sprite.status == 'jump'


def test_player_fall_animation():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    x = 0
    y = 0
    player = pygame.sprite.GroupSingle()
    player_sprite = Player((x, y))
    player.add(player_sprite)
    player.sprite.jump_speed = 5
    player.sprite.update(True, False)
    player.sprite.update(True, False)
    assert player.sprite.status == 'fall'


def test_player_charge():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    x = 0
    y = 0
    player = pygame.sprite.GroupSingle()
    player_sprite = Player((x, y))
    player.add(player_sprite)
    player.sprite.update(False, True)
    player.sprite.update(False, True)
    assert player.sprite.jump_speed == -1


def test_player_charge_and_jump():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    x = 0
    y = 0
    player = pygame.sprite.GroupSingle()
    player_sprite = Player((x, y))
    player.add(player_sprite)
    player.sprite.update(False, True)
    player.sprite.update(True, False)
    assert player.sprite.direction.y == -0.5


def test_next_screen():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    level = Level(load_map("jump/assets/map/game_map.png"), screen)

    level.player.sprite.rect.centery = 900
    level.player.sprite.direction.y = 1
    level.next_screen()

    assert level.world_shift == -600
    assert level.player.sprite.rect.centery == 300

def test_flowing_water():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    slopes = pygame.sprite.Group()
    slope = Slopes((1, 1), 'right')
    slopes.add(slope)
    for sprite in slopes.sprites():
        assert sprite.direction == 'right'
        sprite.update(0)
        assert sprite.frame_index > 0
        assert sprite.image == sprite.animations['flowing_water'][int(sprite.frame_index)]


