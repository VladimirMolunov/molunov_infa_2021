import math
import pygame
from modules import classes
from modules.classes import *
from random import randint, choice

ball_lifetime = 10
ball_r = 10
ball_alpha = 0.1
ball_beta = 0.0005


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
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = self.g
        self.color = color
        self.live = lifetime * self.fps

    def move(self):
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
        Рисует мяч на экране
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
