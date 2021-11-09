import pygame
from random import randint
from pathlib import Path

from modules.classes import Target, Animated, GameObject
from modules.bullets import Bomb
from modules.groups import target_group
from modules.vars import *


class BallTarget(Target):
    def __init__(self, color, min_radius=min_radius, max_radius=max_radius, min_x=min_x, max_x=max_x, min_y=min_y,
                 max_y=max_y, health=ball_health, border=border, show_healthbar=False):
        """
        Конструктор класса мишеней в виде шаров
        :param color: цвет мишени
        :param min_radius: минимальный радиус мишени
        :param max_radius: максимальный радиус мишени
        :param min_x: минимальная координата мишени по горизонтали
        :param max_x: максимальная координата мишени по горизонтали
        :param min_y: минимальная координата мишени по вертикали
        :param max_y: максимальная координата мишени по вертикали
        :param health: количество очков здоровья мишени
        :param border: границапо горизонтали, от которой отражается мишень
        :param show_healthbar: определяет, отображается ли шкала здоровья мишени
        """
        Target.__init__(self, health, border, show_healthbar=show_healthbar)
        self.x = randint(min_x, max_x)
        self.y = randint(min_y, max_y)
        self.vx = randint(-1 * ball_max_x_speed, ball_max_x_speed)
        self.vy = randint(-1 * ball_max_y_speed, ball_max_y_speed)
        self.r = randint(min_radius, max_radius)
        self.color = color

    def draw(self):
        """
        Рисует мишень, возвращает поверхность с ней
        """
        surface = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA)
        surface.fill(transparent)
        pygame.draw.circle(surface, self.color, (self.r, self.r), self.r)
        return surface

    def move_object(self):
        """
        Перемещает мишень по прошествии единицы времени, учитывая отражение от стенок
        """
        if self.r + self.border < self.x + self.vx / self.fps < self.screen_width - self.r:
            self.x += self.vx / self.fps
        else:
            self.vx = - self.vx
            self.x += self.vx / self.fps
        if self.r < self.y + self.vy / self.fps < self.screen_height - self.r:
            self.y += self.vy / self.fps
        else:
            self.vy = - self.vy
            self.y += self.vy / self.fps


class Dragon(Animated):
    def __init__(self, x=dragon_x, y=dragon_y,
                 width=dragon_width, height=dragon_height, period=dragon_period, health=dragon_health):
        """
        Конструктор класса драконов

        :param x: начальная координата центра дракона по горизонтали
        :param y: начальная координата центра дракона по вертикали
        :param width: ширина дракона
        :param height: высота дракона
        :param period: период анимации в секундах
        :param health: здоровье дракона
        """
        Animated.__init__(self, dragon_array, period, red_dragon_array, x, y, health, show_healthbar=True,
                          hit_is_shown=True, hit_time=dragon_hittime)
        self.width = width
        self.height = height

    def move_object(self):
        """
        Перемещает дракона по прошествии единицы времени
        """
        pass


class Plane(GameObject):
    def __init__(self, width=plane_width, height=plane_height, vx=plane_vx,
                 x=None, y=plane_y, health=plane_health, charge=1, show_healthbar=True):
        """
        Конструктор класса истребителей
        :param width: ширина истребителя
        :param height: высота истребителя
        :param vx: скорость истребителя по горизонтали
        :param x: координата центра истребителя по горизонтали
        :param y: координата центра истребителя по верикали
        :param health: здоровье истребителя
        :param charge: количество бомб в запасе у истребителя
        :param show_healthbar: определяет, показывается ли шкала здоровья
        """
        GameObject.__init__(self, x, y, health, show_healthbar)
        if x is None:
            self.x = self.screen_width + 8 * self.healthbar_size
        self.width = width
        self.height = height
        self.vx = vx
        self.charge = charge
        self.image = self.config_image()
        target_group.add(self.sprite)

    def config_image(self):
        surface = plane_image
        surface.set_colorkey(make_transparent)
        surface = pygame.transform.smoothscale(surface, (self.width, self.height))
        return surface

    def move_object(self):
        """
        Перемещает истребитель по прошествии единицы времени
        """
        self.x += self.vx / self.fps

    def fire_bomb(self, lifetime=bomb_lifetime, width=bomb_width, height=bomb_height):
        """
        Производит сбрасывание бомбы
        :param lifetime: время жизни бомбы в секундах
        :param width: длина бомбы
        :param height: толщина бомбы
        :return: новый объект бомбы
        """
        bomb = self.new_bomb(lifetime, width, height, self.x, self.y)
        self.charge -= 1
        return bomb

    @staticmethod
    def new_bomb(lifetime, width, height, x, y, vx=bomb_vx, vy=bomb_vy):
        """
        Создаёт новую бомбу
        :param lifetime: время жизни бомбы в секундах
        :param width: длина бомбы
        :param height: толщина бомбы
        :param x: начальная координата бомбы по горизонтали
        :param y: начальная координата бомбы по вертикали
        :param vx: начальная скорость бомбы по горизонтали
        :param vy: начальная скорость бомбы по вертикали
        :return: новый объект бомбы
        """
        bomb = Bomb(x, y, vx, vy, lifetime, width, height)
        return bomb

    def draw(self):
        """
        Рисует истребитель, возвращает поверхность с ним
        """
        return self.image

    def check_charge(self):
        return True if self.charge > 0 else False


class Fortification(Target):
    def __init__(self, health=fort_health, x=fort_x, y=fort_y, width=fort_width, height=fort_height):
        """
        Конструктор класса вражеских укреплений, по которым стреляет танк
        :param health: здоровье укрепления
        :param x: координата центра укрепления по горизонтали
        :param y: координата центра укрепления по вертикали
        :param width: ширина укрепления
        :param height: высота укрепления
        """
        Target.__init__(self, health, 0, x, y, True)
        self.width = width
        self.height = height
        self.healthbar_size = 12
        self.image = pygame.transform.scale(fort_image, (self.width, self.height))

    def draw(self):
        """
        Рисует укрепление и возвращает поверхность с ним
        """
        return self.image


class Partridge(Animated):
    def __init__(self, x=partridge_x, y=partridge_y, vx=partridge_vx, vy=partridge_vy,
                 width=partridge_width, height=partridge_height, period=partridge_period, health=partridge_health):
        """
        Конструктор класса куропаток

        :param x: начальная координата центра куропатки по горизонтали
        :param y: начальная координата центра куропатки по вертикали
        :param vx: начальная скорость куропатки по горизонтали
        :param vy: начальная скорость куропатки по вертикали
        :param width: ширина куропатки
        :param height: высота куропатки
        :param period: период анимации в секундах
        :param health: здоровье куропатки
        """
        Animated.__init__(self, partridge_array, period, red_partridge_array,
                          x, y, health, hit_is_shown=True, hit_time=partridge_hittime)
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy

    def move_object(self):
        """
        Перемещает куропатку по прошествии единицы времени
        """
        self.x += self.vx / self.fps


class Deer(Animated):
    def __init__(self, x=deer_x, y=deer_y, vx=deer_vx, vy=deer_vy,
                 width=deer_width, height=deer_height, period=deer_period, health=deer_health):
        """
        Конструктор класса оленей

        :param x: начальная координата центра оленя по горизонтали
        :param y: начальная координата центра оленя по вертикали
        :param vx: начальная скорость оленя по горизонтали
        :param vy: начальная скорость оленя по вертикали
        :param width: ширина оленя
        :param height: высота оленя
        :param period: период анимации в секундах
        :param health: здоровье оленя
        """
        Animated.__init__(self, deer_array, period, red_deer_array, x, y, health, show_healthbar=True,
                          hit_is_shown=True, hit_time=deer_hittime)
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy

    def move_object(self):
        """
        Перемещает оленя по прошествии единицы времени
        """
        self.x += self.vx / self.fps


class Hare(Animated):
    def __init__(self, x=hare_x, y=hare_y, vx=hare_vx, vy=hare_vy,
                 width=hare_width, height=hare_height, period=hare_period, health=hare_health):
        """
        Конструктор класса зайцев

        :param x: начальная координата центра зайца по горизонтали
        :param y: начальная координата центра зайца по вертикали
        :param vx: скорость зайца по горизонтали
        :param vy: скорость зайца по вертикали в начале прыжка
        :param width: ширина зайца
        :param height: высота зайца
        :param period: период анимации в секундах
        :param health: здоровье зайца
        """
        Animated.__init__(self, hare_array, period, red_hare_array, x, y, health, show_healthbar=True,
                          hit_is_shown=True, hit_time=deer_hittime)
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy

    def move_object(self):
        """
        Перемещает зайца по прошествии единицы времени
        """
        self.x += self.vx / self.fps
