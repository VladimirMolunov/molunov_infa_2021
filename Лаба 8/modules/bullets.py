import pygame
from pathlib import Path
from math import atan2, pi

from modules.classes import Bullet
from modules.vars import *


class Ball(Bullet):
    def __init__(self, color, lifetime=ball_lifetime, r=ball_r, x=0, y=0, alpha=ball_alpha, beta=ball_beta):
        """
         Конструктор класса мячей, которыми стреляет пушка
        :param color: цвет мяча
        :param lifetime: время жизни мяча в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param r: радиус мяча
        :param x: начальная координата центра мяча по горизонтали
        :param y: начальная координата центра мяча по вертикали
        """
        Bullet.__init__(self, lifetime, alpha, beta, x, y)
        self.r = r
        self.color = color

    def move_object(self):
        """
        Перемещает мяч по прошествии единицы времени, учитывая отражение от стенок
        Переопределяет его скорость в соответствии с силами, действующими на него
        """
        self.ax = - self.alpha * self.vx - self.beta * self.vx * abs(self.vx)
        self.ay = self.g - self.alpha * self.vy - self.beta * self.vy * abs(self.vy)
        self.vx += self.ax / self.fps
        self.vy += self.ay / self.fps
        if self.r < self.x + self.vx / self.fps < self.screen_width - self.r:
            self.x += self.vx / self.fps
        else:
            self.vx = - self.vx
            self.x += self.vx / self.fps
        if self.r < self.y + self.vy / self.fps < self.screen_height - self.r:
            self.y += self.vy / self.fps
        else:
            self.vy = - self.vy
            self.y += self.vy / self.fps

    def draw(self):
        """
        Рисует мяч, возвращает поверхность с ним
        """
        surface = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA)
        surface.fill(transparent)
        pygame.draw.circle(surface, self.color, (self.r, self.r), self.r)
        return surface


class TankShell(Bullet):
    def __init__(self, lifetime=shell_lifetime, h=shell_h, x=0, y=0, alpha=shell_alpha, beta=shell_beta):
        """
         Конструктор класса танковых снарядов, которыми стреляет танк
        :param lifetime: время жизни снаряда в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param h: толщина снаряда
        :param x: начальная координата центра снаряда по горизонтали
        :param y: начальная координата центра снаряда по вертикали
        """
        Bullet.__init__(self, lifetime, alpha, beta, x, y)
        self.h = h
        self.w = tank_shell.get_width() / tank_shell.get_height() * self.h

    def move_object(self):
        """
        Перемещает снаряд по прошествии единицы времени, учитывая отражение от стенок
        Переопределяет его скорость в соответствии с силами, действующими на него
        """
        width = pygame.mask.from_surface(self.draw()).get_size()[0]
        height = pygame.mask.from_surface(self.draw()).get_size()[1]
        self.ax = - self.alpha * self.vx - self.beta * self.vx * abs(self.vx)
        self.ay = self.g - self.alpha * self.vy - self.beta * self.vy * abs(self.vy)
        self.vx += self.ax / self.fps
        self.vy += self.ay / self.fps
        if width / 2 < self.x + self.vx / self.fps < self.screen_width - width / 2:
            self.x += self.vx / self.fps
        else:
            self.vx = - self.vx
            self.x += self.vx / self.fps
        if height / 2 < self.y + self.vy / self.fps < self.screen_height - height / 2:
            self.y += self.vy / self.fps
        else:
            self.vy = - self.vy
            self.y += self.vy / self.fps

    def draw(self):
        """
        Рисует снаряд, возвращает поверхность с ним
        """
        surface = pygame.transform.smoothscale(tank_shell, (int(self.w), int(self.h)))
        surface = pygame.transform.rotate(surface, - atan2(self.vy, self.vx) * 180 / pi)
        return surface
