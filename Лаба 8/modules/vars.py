from pathlib import Path

import pygame.image
from pygame.image import load
from pygame.display import set_mode

# buttons
make_transparent = (255, 255, 255)
screen = set_mode((800, 600))
def_image = load(Path('images', 'def_button.png').resolve()).convert_alpha()
image_pressed = load(Path('images', 'pressed_button.png').resolve()).convert_alpha()
image_pointed = load(Path('images', 'pointed_button.png').resolve()).convert_alpha()

# misc
hare_skin = load(Path('images', 'hare_skin.png').resolve()).convert_alpha()
horns = load(Path('images', 'horns.png').resolve()).convert_alpha()
bird = load(Path('images', 'bird.png').resolve()).convert_alpha()

# groups
transparent = (255, 255, 255, 0)

# menus
button_text_color = (25, 12, 199)
cannon_finish_screen_color = (6, 40, 17)
war_finish_screen_color = (6, 40, 17)
hunt_finish_screen_color = (6, 40, 17)
minecraft_finish_screen_color = (6, 40, 17)
minecraft_lost_color = (6, 40, 17)

# game
target_count = 2
score_for_catch = 1
plane_count = 2
plane_minimum_timeout = 2
plane_chance_per_second = 5

red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
magenta = (255, 3, 184)
cyan = (0, 255, 204)
ball_target_red = (228, 0, 0)
cannon_grey = (102, 102, 102)
cannon_red = (255, 0, 0)
cannon_green = (0, 255, 0)
ball_colors = (red, blue, yellow, green, magenta, cyan)

# classes
FPS = 60
width = 800
height = 600
g = 200
healthbar_image = load(Path('images', 'healthbar.png').resolve()).convert_alpha()
healthbar_inside = load(Path('images', 'healthbar_inside.png').resolve()).convert_alpha()

# bullets
ball_lifetime = 10
ball_r = 10
ball_alpha = 0.1
ball_beta = 0.0005
shell_lifetime = 10
shell_h = 10
tank_shell = load(Path('images', 'tank_shell.png').resolve()).convert_alpha()
shell_alpha = 0.01
shell_beta = 0.0003
bomb_image = load(Path('images', 'bomb.png').resolve()).convert_alpha()
bomb_lifetime = 10
bomb_alpha = 0.001
bomb_beta = 0.00003
bomb_width = 60
bomb_height = 17
bomb_vx = -180
bomb_vy = 200

# targets
min_radius = 20
max_radius = 50
min_x = 500
max_x = 750
min_y = 300
max_y = 550
ball_health = 1
ball_max_x_speed = 300
ball_max_y_speed = 300
border = 450

plane_image = load(Path('images', 'plane.png').resolve()).convert_alpha()
plane_width = 100
plane_height = 35
plane_health = 2
plane_vx = -150
plane_y = 60

fort_image = load(Path('images', 'fort.png').resolve()).convert_alpha()
fort_health = 200
fort_x = 700
fort_y = 350
fort_width = 200
fort_height = 70

dragon_period = 2
dragon_health = 100
dragon_x = 600
dragon_y = 300
dragon_width = 250
dragon_height = 250
dragon_hittime = 1

partridge_period = 1
partridge_health = 1
partridge_x = 850
partridge_y = 70
partridge_vx = -120
partridge_vy = 0
partridge_width = 100
partridge_height = 100
partridge_hittime = 1

deer_period = 1
deer_health = 4
deer_x = 850
deer_y = 450
deer_vx = -80
deer_vy = 0
deer_width = 160
deer_height = 160
deer_hittime = 1

hare_period = 1
hare_health = 2
hare_x = 850
hare_y = 500
hare_vx = -120
hare_vy = 240
hare_width = 60
hare_height = 60
hare_hittime = 1


def get_dragon_array():
    """
    Получает список кадров для анимации дракона
    """
    array = []
    for i in range(1, 58, 1):
        txt = 'frame (' + str(i) + ').gif'
        array.append(load(Path('dragon', txt)))
    return array


def get_red_dragon_array():
    """
    Получает список кадров для анимации дракона, получившего урон
    """
    red_array = []
    for i in range(1, 58, 1):
        txt = 'red (' + str(i) + ').png'
        red_array.append(load(Path('dragon_red', txt)))
    return red_array


def get_partridge_array():
    """
    Получает список кадров для анимации куропатки
    """
    array = []
    for i in range(1, 7, 1):
        txt = str(i) + '.png'
        array.append(load(Path('partridge', txt)))
    return array


def get_red_partridge_array():
    """
    Получает список кадров для анимации куропатки, получившей урон
    """
    red_array = []
    for i in range(1, 7, 1):
        txt = str(i) + '.png'
        red_array.append(load(Path('partridge_red', txt)))
    return red_array


def get_deer_array():
    """
    Получает список кадров для анимации оленя
    """
    array = []
    for i in range(1, 10, 1):
        txt = 'frame-' + str(i) + '.gif'
        array.append(load(Path('deer', txt)))
    return array


def get_red_deer_array():
    """
    Получает список кадров для анимации оленя, получившего урон
    """
    red_array = []
    for i in range(1, 10, 1):
        txt = str(i) + '.png'
        red_array.append(load(Path('deer_red', txt)))
    return red_array


def get_hare_array():
    """
    Получает список кадров для анимации зайца
    """
    array = []
    for i in range(1, 8, 1):
        txt = 'frame-' + str(i) + '.gif'
        array.append(load(Path('hare', txt)))
    return array


def get_red_hare_array():
    """
    Получает список кадров для анимации зайца, получившего урон
    """
    red_array = []
    for i in range(1, 8, 1):
        txt = str(i) + '.png'
        red_array.append(load(Path('hare_red', txt)))
    return red_array


dragon_array = get_dragon_array()
red_dragon_array = get_red_dragon_array()

partridge_array = get_partridge_array()
red_partridge_array = get_red_partridge_array()

deer_array = get_deer_array()
red_deer_array = get_red_deer_array()

hare_array = get_hare_array()
red_hare_array = get_red_hare_array()

# weapons
charge_per_second = 750
max_power = 2000
cannon_x = 20
cannon_y = 450
cannon_width = 30
cannon_height = 20
cannon_default_power = 500
tank_default_power = 2400
tank_x = 225
tank_y = 460
tank_width = 244
tank_height = 88
tank_vx = 50
tank_border = 300
tank_health = 5
tank_image = load(Path('images', 'tank.png').resolve()).convert_alpha()
tank_head_image = load(Path('images', 'tank_head.png').resolve()).convert_alpha()
gun_image = load(Path('images', 'gun.png').resolve()).convert_alpha()
gun_y = 440
gun_default_power = 2400
gun_width = 200
gun_height = 45
gun_delta = 0.366


def sh(surface: pygame.Surface):
    mask = pygame.mask.from_surface(surface)
    w = surface.get_width()
    h = surface.get_height()
    s1 = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(w):
        for j in range(h):
            if mask.get_at((i, j)) == 1:
                s1.set_at((i, j), (255, 0, 0, 128))
    surface.blit(s1, (0, 0))
    return surface


def ch():
    for i in range(1, 8, 1):
        txt = 'frame-' + str(i) + '.gif'
        txt2 = str(i) + '.png'
        p = Path('deer', txt).resolve()
        p2 = Path('deer_red', txt2).resolve()
        a = load(p).convert_alpha()
        pygame.image.save(sh(a), p2)
