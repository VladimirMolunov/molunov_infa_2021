from pathlib import Path
from pygame.image import load
from pygame.display import set_mode

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

# buttons
make_transparent = (255, 255, 255)
screen = set_mode((800, 600))
def_image = load(Path('images', 'def_button.png').resolve()).convert_alpha()
image_pressed = load(Path('images', 'pressed_button.png').resolve()).convert_alpha()
image_pointed = load(Path('images', 'pointed_button.png').resolve()).convert_alpha()

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
dragon_width = 250
dragon_height = 250
dragon_hittime = 1


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


dragon_array = get_dragon_array()
red_dragon_array = get_red_dragon_array()

# weapons
charge_per_second = 750
max_power = 2000
cannon_x = 20
cannon_y = 450
cannon_width = 30
cannon_height = 20
cannon_default_power = 500
tank_default_power = 2400
tank_x = 152
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
