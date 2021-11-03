import pygame
from random import randint

from modules.classes import Target
from modules.groups import transparent

min_radius = 20
max_radius = 50
min_x = 500
max_x = 750
min_y = 300
max_y = 550
health = 1
ball_max_x_speed = 300
ball_max_y_speed = 300
border = 450


class BallTarget(Target):
    def __init__(self, color, min_radius=min_radius, max_radius=max_radius, min_x=min_x, max_x=max_x, min_y=min_y,
                 max_y=max_y, health=health, border=border, show_healthbar=False):
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
        Рисует мишень
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
