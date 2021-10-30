import math
import pygame
from modules import groups
from modules.groups import *
from random import randint, choice

FPS = 60
width = 800
height = 600
g = 200
transparent = (255, 255, 255, 0)


class DrawablesList(list):
    def __init__(self):
        """
        Конструктор класса списков объектов типа Drawable
        """
        list.__init__(self)

    def smart_pop(self, index=-1):
        """
        Убирает объект класса Drawable из соответствующего списка и удаляет его спраайт из всех групп
        :param index: номер элемента, который необходимо убрать, в списке
        """
        self[index].sprite.kill()
        self.pop(index)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(0, 0))


class Showable:
    def __init__(self, width=width, height=height, fps=FPS):
        """
        Конструктор класса объектов, связанных с выводом изображения на экран
        :param width: ширина экрана
        :param height: высота экрана
        :param fps: частота обновления экрана в кадрах в секунду
        """
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.screen_width = width
        self.screen_height = height


class Drawable(Showable):
    def __init__(self, x=0, y=0):
        """
        Конструктор класса объектов игры, изображаемых на экране
        :param x: начальная координата центра объекта по горизонтали
        :param y: начальная координата центра объекта по вертикали
        """
        Showable.__init__(self)
        self.x = x
        self.y = y
        self.sprite = Sprite()
        self.mask = pygame.mask.Mask((0, 0))

    def get_mask(self):
        """
        Получение маски спрайта
        :return: объект маски
        """
        return pygame.mask.from_surface(self.sprite.image)

    def draw(self):
        """
        Рисует объект на поверхности и возвращает эту поверхность
        :return: объект типа pygame.Surface
        """
        return pygame.Surface((0, 0))

    def config_sprite(self):
        """
        Создаёт спрайт с данным объектом и получает его маску
        """
        self.sprite.image = self.draw()
        self.mask = self.get_mask()
        self.sprite.rect = self.sprite.image.get_rect(center=(self.x, self.y))

    def move_object(self):
        """
        Шаблон метода движения объекта
        """
        pass

    def move(self):
        """
        Двигает объект и обновляет его спрайт
        """
        self.move_object()
        self.config_sprite()


class Bullet(Drawable):
    def __init__(self, lifetime, alpha, beta, x=0, y=0, g=g):
        """
        Конструктор класса снарядов
        :param lifetime: время жизни снаряда в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :param x: начальная координата центра снаряда по горизонтали
        :param y: начальная координата центра снаряда по вертикали
        """
        Drawable.__init__(self, x, y)
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.live = lifetime * self.fps
        bullet_group.add(self.sprite)

    def remove_life(self):
        """
        Уменьшает время жизни мяча на 1
        """
        self.live -= 1

    def is_hit(self, target):
        """
        Проверяет, сталкивалкивается ли мяч с мишенью
        :param target: Мишень, с которой проверяется столкновение
        :return: True, если мяч сталкивается с мишенью, False иначе
        """
        return True if (self.x - target.x) ** 2 + (self.y - target.y) ** 2 < (self.r + target.r) ** 2 else False


class Weapon(Drawable):
    def __init__(self, x=0, y=0):
        """
        Конструктор класса стреляющих орудий
        :param x: начальная координата центра орудия по горизонтали
        :param y: начальная координата центра орудия по вертикали
        """
        Drawable.__init__(self, x, y)
        self.is_active = False
        self.angle = 1
        weapon_group.add(self.sprite)

    def charge(self):
        """
        Заряжает орудие
        """
        self.is_active = True


class Target(Drawable):
    def __init__(self, health, x=0, y=0):
        """
        Конструктор класса мишеней
        :param health: количество очков здоровья мишени
        :param x: начальная координата центра мишени по горизонтали
        :param y: начальная координата центра мишени по вертикали
        """
        Drawable.__init__(self, x, y)
        self.health = health
        target_group.add(self.sprite)
