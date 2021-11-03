import pygame
from pathlib import Path

from modules.groups import bullet_group, target_group, healthbar_group, transparent

FPS = 60
width = 800
height = 600
g = 200
healthbar_image = pygame.image.load(Path('images', 'healthbar.png').resolve())


class GameObjectsList(list):
    def __init__(self):
        """
        Конструктор класса списков объектов типа GameObject
        """
        list.__init__(self)

    def smart_pop(self, index=-1):
        """
        Убирает объект класса GameObject из соответствующего списка и удаляет его спраайты из всех групп
        :param index: номер элемента, который необходимо убрать, в списке
        """
        self[index].kill()
        self.pop(index)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса спрайтов
        """
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


class Background(Showable):
    def __init__(self, image):
        """
        Конструктор класса фоновых изображений
        :param image: путь к фоновой картинке
        """
        Showable.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.pos = (0, 0)
        self.config_image(image)

    def config_image(self, image):
        """
        Получает фоновое изображение, оптимизирует его размер и центрирует его на экране
        :param image: путь к фоновой картинке
        """
        self.image = pygame.image.load(image)
        w = self.image.get_width() / self.screen_width
        h = self.image.get_height() / self.screen_height
        if w < h:
            h = int(h * self.screen_height / w)
            w = self.screen_width
            self.pos = (0, (self.screen_height - h) / 2)
        else:
            w = int(w * self.screen_width / h)
            h = self.screen_height
            self.pos = ((self.screen_width - w) / 2, 0)
        self.image = pygame.transform.scale(self.image, (w, h))

    def blit(self):
        """
        Выводит фон на экран
        """
        self.screen.blit(self.image, self.pos)


class GameObject(Showable):
    def __init__(self, x=0, y=0, health=-1, show_healthbar=False, healthbar_size=20, healthbar_gap=0):
        """
        Конструктор класса объектов игры, изображаемых на экране
        :param x: начальная координата центра объекта по горизонтали
        :param y: начальная координата центра объекта по вертикали
        :param health: здоровье объекта (-1 - нет здоровья, объект неуязвим)
        :param show_healthbar: определяет, нужно ли отображать шкалу здоровья объекта
        :param healthbar_size: высота шкалы здоровья
        :param healthbar_gap: зазор между шкалой здоровья и верхним краем объекта
        """
        Showable.__init__(self)
        self.x = x
        self.y = y
        self.health = health
        self.show_healthbar = show_healthbar
        self.healthbar_x = x
        self.healthbar_gap = healthbar_gap
        self.healthbar_y = y
        self.healthbar_size = healthbar_size
        self.sprite = Sprite()
        self.healthbar_sprite = Sprite()
        healthbar_group.add(self.healthbar_sprite)

    def draw(self):
        """
        Рисует объект на поверхности и возвращает эту поверхность
        :return: объект типа pygame.Surface
        """
        return pygame.Surface((0, 0))

    def draw_healthbar(self):
        """
        Рисует шкалу здоровья на поверхности и возвращает эту поверхность
        :return: объект типа pygame.Surface
        """
        surface = healthbar_image.convert_alpha(self.screen)
        surface.set_colorkey(transparent)
        w = int(self.healthbar_size / surface.get_height() * surface.get_width())
        surface = pygame.transform.smoothscale(surface, (w, self.healthbar_size))
        return surface

    def config_sprite(self):
        """
        Создаёт спрайт с данным объектом
        """
        self.sprite.image = self.draw()
        self.sprite.rect = self.sprite.image.get_rect(center=(self.x, self.y))

    def config_healthbar_coords(self):
        """
        Получает координаты шкалы здоровья объекта
        """
        self.healthbar_x = self.x
        self.healthbar_y = self.y - self.draw().get_height() / 2 - self.healthbar_gap - self.healthbar_size / 2

    def config_healthbar_sprite(self):
        """
        Создаёт спрайт со шкалой здоровья объекта
        """
        self.healthbar_sprite.image = self.draw_healthbar()
        self.healthbar_sprite.rect = self.healthbar_sprite.image.get_rect(center=(self.healthbar_x, self.healthbar_y))

    def move_object(self):
        """
        Шаблон метода движения объекта
        """
        pass

    def move(self):
        """
        Двигает объект и обновляет его спрайты
        """
        self.move_object()
        self.config_sprite()
        if self.show_healthbar and self.health >= 0:
            self.config_healthbar_coords()
            self.config_healthbar_sprite()

    def hit(self, damage=1):
        """
        Наносит объекту урон
        :param damage: количество нанесённого урона
        """
        if self.health > 0:
            if self.health - damage <= 0:
                self.health = 0
            else:
                self.health -= damage

    def kill(self):
        """
        Уничтожает объект и удаляет его спрайты
        """
        self.sprite.kill()
        self.healthbar_sprite.kill()


class Bullet(GameObject):
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
        GameObject.__init__(self, x, y)
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = self.g
        self.live = lifetime * self.fps
        bullet_group.add(self.sprite)

    def remove_life(self):
        """
        Уменьшает время жизни мяча на 1
        """
        self.live -= 1

    def is_hit(self, target):
        """
        Проверяет, сталкивалкивается ли снаряд с мишенью
        :param target: Мишень, с которой проверяется столкновение
        :return: True, если снаряд сталкивается с мишенью, False иначе
        """
        return True if pygame.sprite.collide_mask(self.sprite, target.sprite) else False


class Target(GameObject):
    def __init__(self, health, border, x=0, y=0):
        """
        Конструктор класса мишеней
        :param health: количество очков здоровья мишени
        :param border: граница области по горизонтали, которую не может пересекать снаряд
        :param x: начальная координата центра мишени по горизонтали
        :param y: начальная координата центра мишени по вертикали
        """
        GameObject.__init__(self, x, y, health)
        target_group.add(self.sprite)
        self.border = border
