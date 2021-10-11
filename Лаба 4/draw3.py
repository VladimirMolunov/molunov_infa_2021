import pygame
import numpy as np
from pygame.draw import *

pygame.init()

FPS = 30
size = 800  # Глобальная переменная размера
xsize = int(1.8 * size)  # Ширина окошка
ysize = size  # Высота окошка
screen = pygame.display.set_mode((xsize, ysize))

# Объявление цветов
cgreen = (0, 104, 52)
cpink = (255, 176, 129)
cblack = (0, 0, 0)
cwhite = (255, 255, 255)
transparent = (200, 100, 90, 0)

# Некоторые глобальные переменные
xgridstep = 20  # Шаг сетки по x
ygridstep = xgridstep  # Шаг сетки по y
leftmove = size / 200 * - 20  # Смещение левого бамбука вправо
leftup = size / 200 * -10  # Смещение левого бамбука вверх
rightmove = size / 200 * 0  # Смещение правого бамбука вправо
rightup = size / 200 * -10  # Смещение правого бамбука вверх
defaultscale = 1  # Масштаб бамбука

# Заливка полотна розовым
rect(screen, cpink, (0, 0, xsize, ysize))


def leaf(surf, xa, ya, xb, yb):
    """Рисует листик бамбука"""
    ellipse(surf, cgreen, (xa, ya, xb, yb))


def grect(scr, xa, ya, width, height, x):
    """Рисует зелёный прямоугольник, из которых состоит стебель"""
    polygon(scr, cgreen, [(xa, ya), (xa+width*np.cos(x), ya+width*np.sin(x)),
                          (xa + width*np.cos(x) - height * np.sin(x), ya + width * np.sin(x) + height * np.cos(x)),
                          (xa - height*np.sin(x), ya + height * np.cos(x))])


def grid(gridxsize, gridysize, xstep, ystep, addit):
    """Вспомогательная функция, рисует сетку"""
    cgray = (128, 128, 128)
    for i in range(1, int(gridxsize / xstep) + 1, 1):
        pygame.draw.line(screen, cgray, (i * xstep, 0), (i * xstep, gridysize), 1)
    for i in range(1, int(gridysize / ystep) + 1, 1):
        pygame.draw.line(screen, cgray, (0, i * ystep), (gridxsize, i * ystep), 1)
    for i in range(addit, int(gridxsize / xstep) + 1, addit):
        pygame.draw.line(screen, cblack, (i * xstep, 0), (i * xstep, gridysize), 2)
    for i in range(addit, int(gridysize / ystep) + 1, addit):
        pygame.draw.line(screen, cblack, (0, i * ystep), (gridxsize, i * ystep), 2)


def duga(scr, xa, ya, xb, yb, angle1, angle2):
    """Функция дуги эллипса для рисования веток"""
    arc(scr, cgreen, (xa, ya, xb, yb), angle1, angle2, 4)


def duga2(scr, xa, ya, xb, yb, angle1, angle2):
    """Тоже функция дуги эллипса для рисования веток, только толщина поменьше"""
    arc(scr, cgreen, (xa, ya, xb, yb), angle1, angle2, 3)


def drawrightbamboo(right_move, right_up, scale):
    """Рисует правый бамбук"""
    rightbamboo = pygame.Surface((xsize, ysize), pygame.SRCALPHA)

    x1 = size / 200 * 100
    y1 = size / 200 * 150
    w1 = size / 200 * 6
    h1 = size / 200 * 24
    gap = size / 200 * 4  # Просто переменная для подгона значений :)
    initial = size / 200 * 8  # Отвечает за длину двух нижних колен бамбука
    leaflength = size / 8  # Ширина листика
    leafhight = size / 200 * 4  # Длина листика

    grect(rightbamboo, x1, y1 + initial, w1, h1 + initial, 0)
    grect(rightbamboo, x1, y1 - gap - h1, w1, h1 + initial, 0)
    grect(rightbamboo, x1 + w1 + 3 * gap / 4, y1 + gap - 3 * h1, w1, h1 + 3 * gap, np.pi / 12)
    grect(rightbamboo, x1 + 2 * w1 + 3.4 * gap, y1 - gap - 3.4 * h1 - 5 * gap, w1 - gap / 2, h1 + 3.5 * gap, np.pi / 8)

    # Рисование листьев
    surface = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
    rect(surface, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
    leaf(surface, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
    leaf(surface, size / 200 * 20, size / 200 * 28, leaflength, leafhight)
    leaf(surface, size / 200 * 22, size / 200 * 36, leaflength, leafhight)
    leaf(surface, size / 200 * 23, size / 200 * 44, leaflength, leafhight)
    leaf(surface, size / 200 * 22, size / 200 * 56, leaflength, leafhight)

    surface2 = pygame.transform.rotate(surface, 75)
    surface3 = pygame.transform.rotate(surface, -75)
    surface3 = pygame.transform.scale(surface3, (int(size / 8 * 3), int(size / 8 * 3)))
    rightbamboo.blit(surface2, (size / 800 * 24, size / 800 * 50))
    rightbamboo.blit(surface3, (size / 800 * 506, size / 800 * 164))

    threeleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
    rect(threeleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
    leaf(threeleaves, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
    leaf(threeleaves, size / 200 * 18, size / 200 * 30, leaflength, leafhight)
    leaf(threeleaves, size / 200 * 20, size / 200 * 40, leaflength, leafhight)

    threeleaves1 = pygame.transform.rotate(threeleaves, -70)
    threeleaves1 = pygame.transform.scale(threeleaves1, (int(size / 32 * 11), int(size / 32 * 11)))
    threeleaves2 = pygame.transform.rotate(threeleaves, 250)
    threeleaves2 = pygame.transform.scale(threeleaves2, (int(size / 32 * 13), int(size / 32 * 13)))
    rightbamboo.blit(threeleaves1, (size / 200 * 104, size / 200 * 85))
    rightbamboo.blit(threeleaves2, (size / 200 * 19, size / 200 * 98))

    # Рисование веток
    branches = pygame.Surface((size, size), pygame.SRCALPHA)
    rect(branches, transparent, (0, 0, size, size))
    duga(branches, 100, 100, 300, 180, 0.8, 2.4)
    branches1 = pygame.transform.rotate(branches, -30)
    rightbamboo.blit(branches1, (size / 200 * -62, size / 200 * 78))

    rect(branches, transparent, (0, 0, size, size))
    duga(branches, 100, 100, 280, 180, 0.5, 2.5)
    branches1 = pygame.transform.rotate(branches, 30)
    rightbamboo.blit(branches1, (size / 200 * 62, size / 200 * 18))

    rect(branches, transparent, (0, 0, size, size))
    duga(branches, 100, 100, 700, 360, 0.95, 2)
    branches1 = pygame.transform.rotate(branches, 30)
    rightbamboo.blit(branches1, (size / 200 * 29, size / 200 * 10))

    rect(branches, transparent, (0, 0, size, size))
    duga(branches, 100, 100, 700, 360, 1, 2.2)
    branches1 = pygame.transform.rotate(branches, -18)
    rightbamboo.blit(branches1, (size / 200 * -90, size / 200 * -5))

    rightbamboo = pygame.transform.scale(rightbamboo, (int(xsize * scale), int(ysize * scale)))
    screen.blit(rightbamboo, (0 + right_move, 0 + right_up))


def drawleftbamboo(left_move, left_up, scale):
    """Рисует левый бамбук"""
    leftbamboo = pygame.Surface((xsize, ysize), pygame.SRCALPHA)

    x1 = size / 200 * 60
    y1 = size / 200 * 165
    w1 = size / 200 * 3
    h1 = size / 200 * 12
    gap = size / 200 * 2  # Просто переменная для подгона значений :)
    initial = size / 200 * 9  # Отвечает за длину двух нижних колен бамбука
    leafhight = size / 200 * 4  # Длина листика

    grect(leftbamboo, x1, y1 + initial, w1, h1 + initial, 0)
    grect(leftbamboo, x1, y1 - gap - h1, w1, h1 + initial, 0)
    grect(leftbamboo, x1 + w1 + gap / 2, y1 - 4 * gap - 2 * h1, w1, h1 + 2 * gap, np.pi / 12)
    grect(leftbamboo, x1 + 2 * w1 + 3 * gap, y1 - 6 * gap - 2.7 * h1 - 5 * gap, w1 - gap / 2, h1 + 4.5 * gap, np.pi / 8)

    leaflength = size / 6  # Ширина листика

    # Рисование листьев
    threemoreleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
    rect(threemoreleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
    leaf(threemoreleaves, size / 200 * 22, size / 200 * 20, leaflength, leafhight)
    leaf(threemoreleaves, size / 200 * 19, size / 200 * 30, leaflength, leafhight)
    leaf(threemoreleaves, size / 200 * 20, size / 200 * 40, leaflength, leafhight)

    fiveleaves = pygame.Surface((int(size / 8 * 3), int(size / 8 * 3)), pygame.SRCALPHA)
    rect(fiveleaves, transparent, (0, 0, int(size / 8 * 3), int(size / 8 * 3)))
    leaf(fiveleaves, size / 200 * 20, size / 200 * 20, leaflength, leafhight)
    leaf(fiveleaves, size / 200 * 20, size / 200 * 26, leaflength, leafhight)
    leaf(fiveleaves, size / 200 * 22, size / 200 * 32, leaflength, leafhight)
    leaf(fiveleaves, size / 200 * 23, size / 200 * 38, leaflength, leafhight)
    leaf(fiveleaves, size / 200 * 20, size / 200 * 44, leaflength, leafhight)

    fiveleaves1 = pygame.transform.rotate(fiveleaves, -80)
    fiveleaves1 = pygame.transform.scale(fiveleaves1, (int(size / 16 * 3), int(size / 16 * 3)))
    fiveleaves2 = pygame.transform.rotate(fiveleaves, 255)
    fiveleaves2 = pygame.transform.scale(fiveleaves2, (int(size / 14 * 3), int(size / 14 * 3)))
    leftbamboo.blit(fiveleaves1, (size / 800 * 282, size / 800 * 410))
    leftbamboo.blit(fiveleaves2, (size / 800 * 92, size / 800 * 415))

    threemoreleaves1 = pygame.transform.rotate(threemoreleaves, 110)
    threemoreleaves1 = pygame.transform.scale(threemoreleaves1, (int(size / 16 * 3), int(size / 16 * 3)))
    threemoreleaves2 = pygame.transform.rotate(threemoreleaves, 80)
    threemoreleaves2 = pygame.transform.scale(threemoreleaves2, (int(size / 16 * 3), int(size / 16 * 3)))
    leftbamboo.blit(threemoreleaves1, (size / 200 * 58, size / 200 * 131))
    leftbamboo.blit(threemoreleaves2, (size / 200 * 31, size / 200 * 139))

    # Рисование веток
    branches = pygame.Surface((size, size), pygame.SRCALPHA)
    rect(branches, transparent, (0, 0, size, size))
    duga2(branches, 100, 100, 160, 160, 0.2, 2.1)
    branches1 = pygame.transform.rotate(branches, -0)
    leftbamboo.blit(branches1, (size / 200 * -5, size / 200 * 123))

    rect(branches, transparent, (0, 0, size, size))
    duga2(branches, 100, 100, 140, 90, 1, 3)
    branches1 = pygame.transform.rotate(branches, 16)
    leftbamboo.blit(branches1, (size / 200 * 29.5, size / 200 * 74.5))

    rect(branches, transparent, (0, 0, size, size))
    duga2(branches, 100, 100, 200, 90, 0.25, 2.75)
    branches1 = pygame.transform.rotate(branches, 40)
    leftbamboo.blit(branches1, (size / 200 * 23, size / 200 * 6))

    rect(branches, transparent, (0, 0, size, size))
    duga2(branches, 100, 100, 190, 190, 0.5, 2.4)
    branches1 = pygame.transform.rotate(branches, -24)
    leftbamboo.blit(branches1, (size / 200 * -66, size / 200 * 75))

    leftbamboo = pygame.transform.scale(leftbamboo, (int(xsize * scale), int(ysize * scale)))
    screen.blit(leftbamboo, (0 + left_move, 0 + left_up))


def pandahead(right, down, pandascale):
    """Рисует голову панды"""
    pandasize = 800 * pandascale
    panda_head = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_head, cwhite, (450, 500, 170, 200))
    pygame.draw.ellipse(panda_head, cblack, (452, 606, 37, 50))  # Правый глаз
    pygame.draw.ellipse(panda_head, cblack, (515, 612, 50, 50))  # Левый глаз
    pygame.draw.ellipse(panda_head, cblack, (478, 665, 50, 30))  # Нос

    panda_ear = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_ear, cblack, (550, 600, 70, 150))
    panda_ear = pygame.transform.rotate(panda_ear, 30)
    panda_ear = pygame.transform.scale(panda_ear, (int(800), int(800)))
    panda_head.blit(panda_ear, (- pandascale * 20, pandascale * 50))

    panda_ear = pygame.transform.rotate(panda_ear, -70)
    panda_head.blit(panda_ear, (- pandascale * 10, - 220))
    panda_head = pygame.transform.scale(panda_head, (int(pandasize), int(pandasize)))
    screen.blit(panda_head, (right, down))


def panda(right, down, scale):
    """Рисует туловище панды с ногами"""
    panda_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_surface, cwhite, (480, 530, 300, 150))

    panda_leg1 = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_leg1, cblack, (480, 530, 200, 95))
    panda_leg1 = pygame.transform.rotate(panda_leg1, 64)
    panda_surface.blit(panda_leg1, (-60, 240))

    panda_leg2 = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.polygon(panda_leg2, cblack, [(600, 540), (620, 520), (620, 680), (580, 760), (510, 730)])
    panda_surface.blit(panda_leg2, (4, 0))

    panda_leg2_1 = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_leg2_1, cblack, (500, 500, 60, 77))
    panda_leg2_1 = pygame.transform.rotate(panda_leg2_1, 60)
    panda_surface.blit(panda_leg2_1, (-180, 240))

    panda_leg3 = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.polygon(panda_leg3, cblack, [(500, 740), (470, 780), (450, 760), (500, 660)])
    panda_surface.blit(panda_leg3, (4, 0))

    panda_leg3_1 = pygame.Surface((800, 800), pygame.SRCALPHA)
    pygame.draw.ellipse(panda_leg3_1, cblack, (500, 500, 40, 115))
    panda_leg3_1 = pygame.transform.rotate(panda_leg3_1, -5)
    panda_surface.blit(panda_leg3_1, (-68, 113))

    panda_surface = pygame.transform.scale(panda_surface, (int(scale * size), int(scale * size)))
    screen.blit(panda_surface, (right, down))


drawleftbamboo(200, -180, 1)
drawrightbamboo(300, -150, 1)
drawleftbamboo(880, -380, 1.3)
drawrightbamboo(0, 200, 0.5)
panda(300, 0, 1)
pandahead(300, 0, 1)

panda(205, 240, 0.7)
pandahead(210, 250, 0.7)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
