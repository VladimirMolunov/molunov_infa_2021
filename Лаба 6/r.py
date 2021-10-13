import pygame
from pygame.draw import *
pygame.init()
(screen_width, screen_height) = (1200, 750)
screen = pygame.display.set_mode((screen_width, screen_height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIME = (0, 255, 0)
GREEN = (0, 170, 60)
MAGENTA = (255, 0, 255)
VIOLET = (170, 0, 170)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)
BLACK = (0, 0, 0)
transparent = (200, 200, 200, 0)
background = (0, 50, 80)
border = (0, 20, 40)
COLORS = [RED, BLUE, YELLOW, LIME, GREEN, MAGENTA, CYAN, ORANGE, VIOLET]

amogus_red = ((255, 0, 0), (170, 0, 0))
amogus_blue = ((0, 0, 255), (0, 0, 170))
amogus_white = (255, 255, 255)
amogus_gray = (170, 170, 170)
amogus_green = ((0, 255, 0), (0, 170, 0))
amogus_yellow = ((255, 255, 0), (170, 170, 0))
amogus_orange = ((255, 128, 0), (170, 85, 0))
AMOGUS_COLORS = [amogus_red, amogus_blue, (amogus_white, amogus_gray), amogus_green, amogus_yellow, amogus_orange]
(amogus_light, amogus_dark) = ((104, 226, 227), (40, 128, 129))
surf = pygame.Surface((380, 500), pygame.SRCALPHA)
ratio = 19 / 50


def draw_amogus(surface, lightcolor, darkcolor):
    """
    Рисует мишень стандартного размера
    :param surface: поерхность для рисования мишени размера 380x500 пикселей
    :param lightcolor: основной цвет
    :param darkcolor: цвет тени
    """
    rect(surface, lightcolor, (50, 153, 315, 100), 0, -1, -1, 40, -1, 40)
    ellipse(surface, darkcolor, (180, 195, 240, 268))
    rect(surface, transparent, (0, 376, 380, 124))
    rect(surface, transparent, (365, 340, 15, 40))
    rect(surface, BLACK, (50, 153, 330, 238), 15, 40, -1, 40, -1, 40)
    circle(surface, BLACK, (170, 140), 140)
    rect(surface, BLACK, (30, 140, 280, 253))
    circle(surface, lightcolor, (170, 140), 125)
    rect(surface, lightcolor, (45, 140, 250, 253))


def drawamogus(surface, color, height, right_orientation):
    """
    Рисует мишень заданного размера
    :param surface: поерхность для рисования мишени
    :param color: кортеж цветов мишени
    :param height: высота мишени
    :param right_orientation: ориентация по горизонтали: вправо - True, влево - False
    """
    draw_amogus(surface, color[0], color[1])
    if right_orientation:
        surface = pygame.transform.flip(surface, True, False)
    surface = pygame.transform.scale(surface, (int(height * ratio * 2), height))


drawamogus(surf, amogus_green, 200, False)
screen.fill(amogus_white)
screen.blit(surf, (500, 0))
pygame.display.update()
clock = pygame.time.Clock()
finished = False
tickcount = 0

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
