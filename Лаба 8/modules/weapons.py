import math
import pygame
from modules import classes
from modules import bullets
from modules.classes import *
from random import randint, choice

charge_per_second = 500
max_power = 2000
gun_x = 20
gun_y = 450
gun_width = 20
gun_height = 10
gun_default_power = 500


class Gun(Weapon):
    def __init__(self, gun_color, charged_color, width=gun_width, height=gun_height,
                 default_power=gun_default_power):
        """
        Конструктор класса пушек
        :param gun_color: цвет пушки
        :param charged_color: цвет заряженной пушки
        :param width: ширина пушки
        :param height: высота пушки
        :param default_power: скорость мяча, только что вылетевшего из пушки
        """
        Weapon.__init__(self, gun_x, gun_y)
        self.power = default_power
        self.color = gun_color
        self.gun_color = gun_color
        self.charged_color = charged_color
        self.width = width
        self.height = height
        self.default_power = default_power

    def fire_ball(self, event, colors, lifetime=bullets.ball_lifetime, r=bullets.ball_r):
        """
        Производит выстрел
        :param event: событие отпускания кнопки мыши
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :return: новый объект мяча
        """
        ball = self.new_ball(event, choice(colors), lifetime, r,
                             self.x + self.width * math.cos(self.angle), self.y + self.height * math.sin(self.angle))
        self.is_active = False
        self.power = self.default_power
        return ball

    def new_ball(self, event, color, lifetime, r, x, y):
        """
        Создаёт новый мяч после выстрела
        :param event: событие отпускания кнопки мыши
        :param color: цвет мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        :return: новый объект мяча
        """
        ball = bullets.Ball(color, lifetime, r, x, y)
        self.angle = math.atan2((event.pos[1] - ball.y), (event.pos[0] - ball.x))
        ball.vx = self.power * math.cos(self.angle)
        ball.vy = self.power * math.sin(self.angle)
        return ball

    def targetting(self, event: pygame.event.Event):
        """
        Направление пушки в зависимости от положения курсора (прицеливание)
        :param event: событие перемещения мыши
        """
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] == self.x:
                if event.pos[1] > self.y:
                    self.angle = math.pi / 2
                else:
                    self.angle = - math.pi / 2
            else:
                self.angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        self.define_color()

    def define_color(self):
        """
        Переопределяет цвет пушки в зависимости от того, заряжена ли она
        """
        if self.is_active:
            self.color = self.charged_color
        else:
            self.color = self.gun_color

    def draw(self):
        """
        Рисует пушку
        """
        height = self.height / 2
        width = self.width
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        x1 = self.x + height * s
        x2 = self.x - height * s
        x3 = self.x - height * s + width * c
        x4 = self.x + height * s + width * c
        y1 = self.y - height * c
        y2 = self.y + height * c
        y3 = self.y + height * c + width * s
        y4 = self.y - height * c + width * s
        pygame.draw.polygon(self.screen, self.color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def power_up(self, charge_per_second=charge_per_second, max_power=max_power):
        """
        Добавляет определённое значение к заряду пушки, если она уже заряжена и её заряд меньше максимально допустимого
        Необходимое значение рассчитывается для одного кадра
        :param max_power: максимально допустимый заряд пушки
        :param charge_per_second: заряд, который пушка получает за секунду
        """
        if self.is_active and self.power < max_power:
            self.power += charge_per_second / self.fps
        self.define_color()
