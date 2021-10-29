import math
import pygame
from random import randint, choice

FPS = 60
width = 800
height = 600
g = 200


class Sprite(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()


class Drawable:
    def __init__(self, width=width, height=height, fps=FPS):
        """
        Конструктор класса объектов, изображаемых на экране
        :param width: ширина экрана
        :param height: высота экрана
        :param fps: частота обновления экрана в кадрах в секунду
        """
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.screen_width = width
        self.screen_height = height


class Bullet(Drawable):
    def __init__(self, lifetime, alpha, beta, x, y, g=g):
        """
        Конструктор класса снарядов
        :param lifetime: время жизни снаряда в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :param x: начальная координата центра снаряда по горизонтали
        :param y: начальная координата центра снаряда по вертикали
        """
        Drawable.__init__(self)
        self.g = g
        self.x = x
        self.y = y
        self.alpha = alpha
        self.beta = beta
        self.live = lifetime * self.fps
        self.sprite = pygame.sprite.Sprite()

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
    def __init__(self, x, y):
        """
        Конструктор класса стреляющих орудий
        :param x: координата центра вращения орудия по горизонтали
        :param y: координата центра вращения орудия по вертикали
        """
        Drawable.__init__(self)
        self.x = x
        self.y = y
        self.is_active = False
        self.angle = 1

    def charge(self):
        """
        Заряжает орудие
        """
        self.is_active = True


class Target(Drawable):
    def __init__(self, health):
        """
        Конструктор класса мишеней
        :param health: количество очков здоровья мишени
        """
        Drawable.__init__(self)
        self.health = health
