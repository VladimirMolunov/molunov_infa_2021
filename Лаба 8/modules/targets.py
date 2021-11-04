import pygame
from random import randint
from pathlib import Path

from modules.classes import Target, Animated
from modules.groups import transparent

min_radius = 20
max_radius = 50
min_x = 500
max_x = 750
min_y = 300
max_y = 550
ball_health = 1
ball_max_x_speed = 300
ball_max_y_speed = 300
border = 450

dragon_period = 2
dragon_health = 100
dragon_width = 250
dragon_height = 250
dragon_hittime = 1


class BallTarget(Target):
    def __init__(self, color, min_radius=min_radius, max_radius=max_radius, min_x=min_x, max_x=max_x, min_y=min_y,
                 max_y=max_y, health=ball_health, border=border, show_healthbar=False):
        """
        Конструктор класса мишеней
        :param color: цвет мишени
        :param min_radius: минимальный радиус мишени
        :param max_radius: максимальный радиус мишени
        :param min_x: минимальная координата мишени по горизонтали
        :param max_x: максимальная координата мишени по горизонтали
        :param min_y: минимальная координата мишени по вертикали
        :param max_y: максимальная координата мишени по вертикали
        :param health: количество очков здоровья мишени
        """
        Target.__init__(self, health, border)
        self.x = randint(min_x, max_x)
        self.y = randint(min_y, max_y)
        self.vx = randint(-1 * ball_max_x_speed, ball_max_x_speed)
        self.vy = randint(-1 * ball_max_y_speed, ball_max_y_speed)
        self.r = randint(min_radius, max_radius)
        self.color = color
        self.show_healthbar = show_healthbar

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
    def __init__(self, width=dragon_width, height=dragon_height, period=dragon_period, health=dragon_health):
        """
        Конструктор класса драконов

        :param width: ширина дракона
        :param height: высота дракона
        :param period: период анимации в секундах
        :param health: здоровье дракона
        """
        Animated.__init__(self, self.get_array(), period, self.get_red_array(), 600, 300, health, True,
                          hit_is_shown=True, hit_time=dragon_hittime)
        self.width = width
        self.height = height

    @staticmethod
    def get_array():
        """
        Получает список кадров для анимации дракона
        """
        dragon_array = []
        for i in range(1, 58, 1):
            txt = 'frame (' + str(i) + ').gif'
            dragon_array.append(pygame.image.load(Path('dragon', txt)))
        return dragon_array

    @staticmethod
    def get_red_array():
        """
        Получает список кадров для анимации дракона, получившего урон
        """
        red_dragon_array = []
        for i in range(1, 58, 1):
            txt = 'red (' + str(i) + ').png'
            red_dragon_array.append(pygame.image.load(Path('dragon_red', txt)))
        return red_dragon_array

    def draw(self):
        """
        Рисует дракона, возвращает поверхность с ним
        """
        if self.hit_is_shown and self.hit_timeleft > 0:
            surface = self.red_image_array[self.get_frame_number()]
        else:
            surface = self.image_array[self.get_frame_number()]
        surface = pygame.transform.scale(surface, (self.width, self.height)).convert_alpha()
        return surface

    def move_object(self):
        """
        Перемещает дракона по прошествии единицы времени
        """
        pass
