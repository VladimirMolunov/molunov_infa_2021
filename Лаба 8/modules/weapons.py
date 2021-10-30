from math import cos, sin, atan2, pi
import pygame
from random import choice

from modules.bullets import ball_lifetime, ball_r, Ball
from modules.groups import transparent, weapon_group
from modules.classes import Drawable

x = 20
y = 450
charge_per_second = 750
max_power = 2000
gun_x = 20
gun_y = 450
gun_width = 30
gun_height = 20
gun_default_power = 500


class Weapon(Drawable):
    def __init__(self, power, x=0, y=0):
        """
        Конструктор класса стреляющих орудий
        :param x: начальная координата центра орудия по горизонтали
        :param y: начальная координата центра орудия по вертикали
        """
        Drawable.__init__(self, x, y)
        self.is_active = False
        self.power = power
        self.angle = 1
        weapon_group.add(self.sprite)

    def charge(self):
        """
        Заряжает орудие
        """
        self.is_active = True

    def fire_ball(self, event, colors, lifetime=ball_lifetime, r=ball_r):
        """
        Производит выстрел
        :param event: событие отпускания кнопки мыши
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :return: новый объект мяча
        """
        ball = self.new_ball(event, choice(colors), lifetime, r,
                             self.x + self.width * cos(self.angle), self.y + self.height * sin(self.angle))
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
        ball = Ball(color, lifetime, r, x, y)
        self.angle = atan2((event.pos[1] - ball.y), (event.pos[0] - ball.x))
        ball.vx = self.power * cos(self.angle)
        ball.vy = self.power * sin(self.angle)
        return ball


class SimpleCannon(Weapon):
    def __init__(self, gun_color, charged_color, fully_charged_color, width=gun_width, height=gun_height,
                 default_power=gun_default_power, max_power=max_power, charge_per_second=charge_per_second):
        """
        Конструктор класса пушек
        :param gun_color: цвет пушки
        :param charged_color: цвет заряженной пушки
        :param fully_charged_color: цвет полностью заряженной пушки
        :param width: ширина пушки
        :param height: высота пушки
        :param default_power: скорость мяча, только что вылетевшего из пушки
        :param max_power: максимально допустимый заряд пушки
        :param charge_per_second: заряд, который пушка получает за секунду
        """
        Weapon.__init__(self, default_power, gun_x, gun_y)
        self.color = gun_color
        self.gun_color = gun_color
        self.charged_color = charged_color
        self.fully_charged_color = fully_charged_color
        self.width = width
        self.height = height
        self.default_power = default_power
        self.max_power = max_power
        self.charge_per_second = charge_per_second

    def targetting(self, event: pygame.event.Event):
        """
        Направление пушки в зависимости от положения курсора (прицеливание)
        :param event: событие перемещения мыши
        """
        if event.type == pygame.MOUSEMOTION:
            self.angle = atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.define_color()

    def define_color(self):
        """
        Переопределяет цвет пушки в зависимости от того, насколько она заряжена (и заряжена ли вообще)
        """
        if self.is_active:
            p = (self.power - self.default_power) / (self.max_power - self.default_power)
            rgb = []
            for i in range(3):
                rgb.append(min(max(int((self.charged_color[i] * (1 - p) + self.fully_charged_color[i] * p) *
                                       (2.3 * p - 2.3 * p ** 2 + 1)), 0), 255))
            self.color = (rgb[0], rgb[1], rgb[2])
        else:
            self.color = self.gun_color

    def draw(self):
        """
        Рисует пушку
        """
        r = max(self.width, self.height)
        w = self.width
        h = self.height
        surface = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
        surface.fill(transparent)
        pygame.draw.rect(surface, self.color, (r - w, r - h, 2 * w, 2 * h))
        surface = pygame.transform.scale(surface, (r, r))
        surface = pygame.transform.rotate(surface, -1 * self.angle * 180 / pi)
        return surface

    def power_up(self):
        """
        Добавляет определённое значение к заряду пушки, если она уже заряжена и её заряд меньше максимально допустимого
        Необходимое значение рассчитывается для одного кадра
        """
        if self.is_active and self.power < self.max_power:
            self.power += self.charge_per_second / self.fps
        self.define_color()
