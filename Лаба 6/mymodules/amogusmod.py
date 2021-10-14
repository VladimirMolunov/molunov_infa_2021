import pygame
from pygame.draw import *
from random import randint
pygame.init()
amogus_surface_list = []


def defsurfacelist(max_number_of_amogus, max_height, transparent, amogus_list, amogus, amogus_red):
    global amogus_surface_list
    for i in range(0, max_number_of_amogus, 1):
        amogus_surface_list.append(pygame.Surface((2 * max_height, 2 * max_height), pygame.SRCALPHA))
        amogus_surface_list[-1].fill(transparent)
        amogus_list.append(amogus(False, True, True, 0, 0, 0, 0, 0, amogus_red, amogus_surface_list[i], 0))


class Amogus:
    """
    Другой тип мишеней
    :param initialised: определяет, создана ли уже эта мишень (True) или объект является "пустышкой" (False)
    :param status: определяет, должна ли мишень быть видима на экране
    :param faces_right: определяет ориентацию мишени по горизонтали: вправо - True, влево - False
    :param x: координата центра мишени по горизонтали
    :param y: координата центра мишени по вертикали
    :param r: высота мишени
    :param vx: скорость мишени по горизонтали
    :param vy: скорость мишени по вертикали
    :param color: кортеж цветов мишени
    :param surface: поверхность, на которой нарисована мишень
    :param timeleft: оставшееся время жизни мишени (в кадрах)
    """
    def __init__(self, initialised, status, faces_right, x, y, r, vx, vy, color, surface, timeleft):
        self.initialised = initialised
        self.status = status
        self.faces_right = faces_right
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.surface = surface
        self.timeleft = timeleft

    def rotate(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

    def moveamogus(self, velx, vely, time, left_border, right_border, top_border, bottom_border, ratio):
        """
        Двигает мишень в соответствии с заданной скоростью
        velx - скорость по x в секунду
        vely - скорость по y в секунду
        time - время одного обновления экрана
        При необходимости осуществляет отражение мишени от стенок с координатами:
        left_border (координата x левой границы), right_border (координата x правой границы),
        top_border (координата y верхней границы), bottom_border (координата y нижней границы)
        ratio - отношение высоты мишени к половине её ширины
        """
        if right_border - int(self.r * ratio) > (self.x + velx * time) > left_border + int(self.r * ratio):
            self.x += velx * time
        else:
            self.vx = -1 * self.vx
            velx = -1 * velx
            self.x += velx * time
            self.faces_right = True if (self.vx > 0) else False
            self.rotate()

        if bottom_border - int(self.r / 2) > (self.y + vely * time) > top_border + int(self.r / 2):
            self.y += vely * time
        else:
            self.vy = -1 * self.vy
            vely = -1 * vely
            self.y += vely * time


def draw_amogus(surface, lightcolor, darkcolor, transparent, black, amogus_dark, amogus_light, amogus_white):
    """
    Рисует мишень стандартного размера
    :param surface: поерхность для рисования мишени размера 380x500 пикселей
    :param lightcolor: основной цвет
    :param darkcolor: цвет тени
    """
    surface1 = pygame.Surface((280, 398), pygame.SRCALPHA)
    surface2 = pygame.Surface((500, 900), pygame.SRCALPHA)
    surface3 = pygame.Surface((280, 120), pygame.SRCALPHA)
    surface1.fill(transparent)
    rect(surface1, darkcolor, (15, 0, 250, 398))
    ellipse(surface2, lightcolor, (115, 115, 275, 478))
    surface2 = pygame.transform.rotate(surface2, -10)
    surface1.blit(surface2, (-222, -260))
    rect(surface1, transparent, (0, 0, 280, 70))
    rect(surface1, transparent, (0, 0, 15, 390))
    surface3.fill(transparent)
    ellipse(surface3, black, (0, 0, 280, 240), 15)

    rect(surface, lightcolor, (50, 153, 315, 100), 0, -1, 0, 40, 0, 40)
    ellipse(surface, darkcolor, (180, 195, 240, 268))
    rect(surface, transparent, (0, 376, 380, 124))
    rect(surface, transparent, (365, 340, 15, 40))
    rect(surface, black, (50, 153, 330, 238), 15, 40, 0, 40, 0, 40)
    ellipse(surface, lightcolor, (30, 0, 280, 240))
    ellipse(surface, darkcolor, (190, 360, 120, 140))
    rect(surface, black, (190, 300, 120, 130))
    rect(surface, black, (30, 350, 114, 64))
    rect(surface, black, (30, 120, 280, 273))
    ellipse(surface, black, (190, 360, 120, 140), 15)
    rect(surface, darkcolor, (206, 363, 89, 67))
    ellipse(surface, darkcolor, (30, 334, 114, 160))
    ellipse(surface, black, (30, 334, 114, 160), 15)
    rect(surface, darkcolor, (45, 363, 84, 41))
    rect(surface, darkcolor, (45, 363, 250, 50))
    rect(surface, black, (129, 398, 77, 15), 0, -1, 10, 10, 0, 0)
    surface.blit(surface1, (30, 0))
    surface.blit(surface3, (30, 0))
    ellipse(surface, amogus_dark, (0, 83, 230, 150))
    ellipse(surface, amogus_light, (25, 95, 150, 91))
    ellipse(surface, amogus_white, (45, 112, 100, 41))
    ellipse(surface, black, (0, 83, 230, 150), 15)


def drawamogus(surface, color, height, right_orientation, ratio, transparent, black, amogus_dark, amogus_light,
               amogus_white):
    """
    Рисует мишень заданного размера и возвращает поверхность с ней
    :param surface: поерхность для рисования мишени
    :param color: кортеж цветов мишени
    :param height: высота мишени
    :param right_orientation: ориентация по горизонтали: вправо - True, влево - False
    """
    draw_amogus(surface, color[0], color[1], transparent, black, amogus_dark, amogus_light, amogus_white)
    if right_orientation:
        surface = pygame.transform.flip(surface, True, False)
    scaled_surface = pygame.transform.scale(surface, (int(height * ratio * 2), height))
    return scaled_surface


def new_amogus(amoguslist, min_height, max_height, leftborder, rightborder, topborder, bottomborder, ratio,
               min_amogus_speed, max_amogus_speed, amogus_colors, amogus_lifetime, tps, transparent, black,
               amogus_dark, amogus_light, amogus_white):
    """
    Рисует новую мишень со случайными координатами и высотой
    Добавляет его параметры в список amoguslist
    """
    global amogus_surface_list
    h = randint(min_height, max_height)
    x = randint(leftborder + int(ratio * h), rightborder - int(ratio * h))
    y = randint(topborder + int(h / 2), bottomborder - int(h / 2))
    vertical = randint(0, 1)
    horizontal = randint(0, 1)
    vx = randint(min_amogus_speed, max_amogus_speed)
    if horizontal == 1:
        vx = -1 * vx
    orientated_right = True if (vx > 0) else False
    vy = randint(min_amogus_speed, max_amogus_speed)
    if vertical == 1:
        vy = -1 * vy
    color = amogus_colors[randint(0, len(amogus_colors)) - 1]
    amogus_surface_list.pop(0)
    amogus_surface_list.append(pygame.Surface((380, 500), pygame.SRCALPHA))
    amoguslist.append(Amogus(True, True, orientated_right, x, y, h, vx, vy, color, amogus_surface_list[-1],
                             amogus_lifetime * tps))
    amoguslist.pop(0)
    newamogus = amoguslist[-1]
    newamogus.surface.fill(transparent)
    newamogus.surface = drawamogus(newamogus.surface, newamogus.color, newamogus.r, newamogus.faces_right,
                                   ratio, transparent, black, amogus_dark, amogus_light, amogus_white)
