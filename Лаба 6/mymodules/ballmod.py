import pygame
from pygame.draw import *
from random import randint
pygame.init()
surface_list = []


def defsurfacelist(max_number_of_balls, max_radius, transparent, ball_list, black):
    global surface_list
    for i in range(0, max_number_of_balls, 1):
        surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
        surface_list[-1].fill(transparent)
        ball_list.append(Ball(False, True, 0, 0, 0, 0, 0, black, surface_list[i]))


class Ball:
    """
    Класс шариков
    :param initialised: определяет, создан ли уже этот шарик (True) или объект является "пустышкой" (False)
    :param status: определяет, должен ли шарик быть видим на экране
    :param x: координата центра шарика по горизонтали
    :param y: координата центра шарика по вертикали
    :param r: радиус шарика
    :param vx: скорость шарика по горизонтали
    :param vy: скорость шарика по вертикали
    :param color: цвет шарика
    :param surface: поверхность, на которой нарисован шарик
    """
    def __init__(self, initialised, status, x, y, r, vx, vy, color, surface):
        self.initialised = initialised
        self.status = status
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.surface = surface

    def moveball(self, velx, vely, time, left_border, right_border, top_border, bottom_border):
        """
        Двигает шарик в соответствии с заданной скоростью
        velx - скорость по x в секунду
        vely - скорость по y в секунду
        time - время одного обновления экрана
        При необходимости осуществляет отражение шарика от стенок с координатами:
        left_border (координата x левой границы), right_border (координата x правой границы),
        top_border (координата y верхней границы), bottom_border (координата y нижней границы).
        """
        if right_border - self.r > (self.x + velx * time) > left_border + self.r:
            self.x += velx * time
        else:
            self.vx = -1 * self.vx
            velx = -1 * velx
            self.x += velx * time

        if bottom_border - self.r > (self.y + vely * time) > top_border + self.r:
            self.y += vely * time
        else:
            self.vy = -1 * self.vy
            vely = -1 * vely
            self.y += vely * time


def new_ball(balllist, min_radius, max_radius, leftborder, rightborder, topborder, bottomborder, max_speed, colors,
             transparent):
    """
    Рисует новый шарик со случайными координатами и радиусом
    Добавляет его параметры в список balllist
    min_radius - минимальный радиус шарика
    max_radius - максимальный радиус шарика
    leftborder, rightborder, topborder, bottomborder - координаты стенок
    max_speed - максимальная скорость шарика
    colors - кортеж возможных цветов шарика
    transparent - прозрачный цвет
    """
    global surface_list
    r = randint(min_radius, max_radius)
    x = randint(leftborder + r, rightborder - r)
    y = randint(topborder + r, bottomborder - r)
    vx = randint(-1 * max_speed, max_speed)
    vy = randint(-1 * max_speed, max_speed)
    color = colors[randint(0, len(colors)) - 1]
    surface_list.pop(0)
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    balllist.append(Ball(True, True, x, y, r, vx, vy, color, surface_list[-1]))
    balllist.pop(0)
    newball = balllist[-1]
    newball.surface.fill(transparent)
    circle(newball.surface, newball.color, (max_radius, max_radius), newball.r)
