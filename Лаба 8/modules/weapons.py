from math import cos, sin, atan2, pi
import pygame
from pathlib import Path
from random import choice

from modules.bullets import ball_lifetime, ball_r, Ball
from modules.groups import transparent, weapon_group
from modules.classes import Drawable

charge_per_second = 750
max_power = 2000
cannon_x = 20
cannon_y = 450
cannon_width = 30
cannon_height = 20
cannon_default_power = 500
tank_default_power = 2400
tank_width = 244
tank_height = 88
tank_vx = 50
tank_image = pygame.image.load(Path('images', 'tank.png').resolve())
tank_head_image = pygame.image.load(Path('images', 'tank_head.png').resolve())


class Weapon(Drawable):
    def __init__(self, default_power, x=0, y=0):
        """
        Конструктор класса стреляющих орудий
        :param x: начальная координата центра орудия по горизонтали
        :param y: начальная координата центра орудия по вертикали
        """
        Drawable.__init__(self, x, y)
        self.is_active = False
        self.power = default_power
        self.default_power = default_power
        self.angle = 0
        self.head_x = 0
        self.head_y = 0
        weapon_group.add(self.sprite)

    def charge(self):
        """
        Заряжает орудие
        """
        self.is_active = True

    def fire_ball(self, colors, lifetime=ball_lifetime, r=ball_r):
        """
        Производит выстрел
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :return: новый объект мяча
        """
        ball = self.new_ball(choice(colors), lifetime, r, self.head_x, self.head_y, self.angle)
        self.is_active = False
        self.power = self.default_power
        return ball

    def new_ball(self, color, lifetime, r, x, y, angle):
        """
        Создаёт новый мяч
        :param color: цвет мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        :param angle: угол наклона начальной скорости шарика к горизонтальной оси, направленной вправо
        (против часовой стрелки)
        :return: новый объект мяча
        """
        ball = Ball(color, lifetime, r, x, y)
        ball.vx = self.power * cos(angle)
        ball.vy = self.power * sin(angle)
        return ball


class SimpleCannon(Weapon):
    def __init__(self, cannon_color, charged_color, fully_charged_color, width=cannon_width, height=cannon_height,
                 default_power=cannon_default_power, max_power=max_power, charge_per_second=charge_per_second):
        """
        Конструктор класса пушек
        :param cannon_color: цвет пушки
        :param charged_color: цвет заряженной пушки
        :param fully_charged_color: цвет полностью заряженной пушки
        :param width: ширина пушки
        :param height: высота пушки
        :param default_power: скорость снаряда, только что вылетевшего из пушки
        :param max_power: максимально допустимый заряд пушки
        :param charge_per_second: заряд, который пушка получает за секунду
        """
        Weapon.__init__(self, default_power, cannon_x, cannon_y)
        self.color = cannon_color
        self.cannon_color = cannon_color
        self.charged_color = charged_color
        self.fully_charged_color = fully_charged_color
        self.width = width
        self.height = height
        self.default_power = default_power
        self.max_power = max_power
        self.charge_per_second = charge_per_second
        self.head_x = self.x + self.width * cos(self.angle)
        self.head_y = self.y + self.height * sin(self.angle)

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
            self.color = self.cannon_color

    def targetting(self, event: pygame.event.Event):
        """
        Изменение направления пушки в зависимости от положения курсора (прицеливание)
        :param event: событие перемещения мыши
        """
        if event.type == pygame.MOUSEMOTION:
            self.angle = atan2((event.pos[1] - self.y), (event.pos[0] - self.x))

    def draw(self):
        """
        Рисует пушку, возвращает поверхность с ней
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


class Tank(Weapon):
    """
    Конструктор класса танков
    :param width: ширина танка
    :param height: высота танка
    :param default_power: скорость снаряда, только что вылетевшего из танка
    """
    def __init__(self, width=tank_width, height=tank_height, power=tank_default_power, vx=tank_vx):
        Weapon.__init__(self, power, 80, 460)
        self.width = width
        self.height = height
        self.vx = vx
        self.speed = 0
        self.visible_speed = 0
        self.orientated_right = True
        self.head_angle = self.angle

    def get_speed(self):
        """
        Устанавливает скорость движения танка
        """
        if -self.vx <= self.speed <= self.vx:
            self.visible_speed = self.speed
        elif self.speed > self.vx:
            self.visible_speed = self.vx
        elif self.speed < -self.vx:
            self.visible_speed = -self.vx

    def move_object(self):
        """
        Перемещает танк по прошествии единицы времени
        """
        self.get_speed()
        self.x += self.visible_speed / self.fps
        self.get_head_coords()

    def draw(self):
        """
        Рисует танк, возвращает поверхность с ним
        """
        tank = tank_image.convert_alpha(self.screen)
        tank_head = tank_head_image.convert_alpha(self.screen)
        tank = pygame.transform.smoothscale(tank, (self.width, self.height))
        tank_head = pygame.transform.smoothscale(tank_head, (self.width, self.height))
        tank_head = pygame.transform.rotate(tank_head, - 180 / pi * self.head_angle)
        surface = pygame.Surface((2 * self.width, 2 * self.height), pygame.SRCALPHA)
        surface.fill(transparent)
        surface.blit(tank, (self.width / 2, self.height / 2))
        xa = 691/610 * self.width
        ya = 166/220 * self.height
        xw = 386/610 * self.width
        yw = 56/220 * self.height
        xv = xw - self.width
        yv = yw - self.height
        s = sin(self.head_angle)
        c = cos(self.head_angle)
        x0 = - xw * c + yw * s
        y0 = - xw * s - yw * c
        x1 = - xw * c + yv * s
        y1 = - xw * s - yv * c
        x2 = - xv * c + yv * s
        y2 = - xv * s - yv * c
        x3 = - xv * c + yw * s
        y3 = - xv * s - yw * c
        head_x = xa + min(x0, x1, x2, x3)
        head_y = ya + min(y0, y1, y2, y3)
        surface.blit(tank_head, (head_x, head_y))
        if self.orientated_right:
            surface = pygame.transform.flip(surface, True, False)
        return surface

    def targetting(self, event: pygame.event.Event):
        """
        Изменение направления башни танка в зависимости от положения курсора (прицеливание)
        :param event: событие перемещения мыши
        """
        if event.type == pygame.MOUSEMOTION:
            if self.orientated_right:
                self.head_angle = - atan2((event.pos[1] - self.y), (event.pos[0] - self.x)) / 6
                if self.head_angle < -pi / 24:
                    self.head_angle = -pi / 24
                if self.head_angle > pi / 12:
                    self.head_angle = pi / 12
                self.angle = - self.head_angle
            else:
                self.head_angle = - atan2((event.pos[1] - self.y), (self.x - event.pos[0])) / 6
                if self.head_angle < -pi / 24:
                    self.head_angle = -pi / 24
                if self.head_angle > pi / 12:
                    self.head_angle = pi / 12
                self.angle = pi + self.head_angle

    def get_head_coords(self):
        """
        Получает координаты конца дула (начальной точки движения вылетающих снарядов)
        """
        z = self.width * (81/610 - 386/610 * cos(self.head_angle)) + 3/110 * self.height * sin(self.head_angle)
        if self.orientated_right:
            self.head_x = self.x - z
        else:
            self.head_x = self.x + z
        self.head_y = self.y - self.height * (27/110 + 3/110 *
                                              cos(self.head_angle)) - 386/610 * self.width * sin(self.head_angle)

    def add_left_speed(self):
        """
        Добавляет скорость танка влево
        """
        self.speed -= self.vx

    def add_right_speed(self):
        """
        Добавляет скорость танка вправо
        """
        self.speed += self.vx
