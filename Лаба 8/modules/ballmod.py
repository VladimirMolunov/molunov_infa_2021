import math
import pygame
from random import randint, choice
FPS = 60


class Drawable:
    def __init__(self, width=800, height=600, fps=FPS):
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


class Ball(Drawable):
    def __init__(self, colors: list, lifetime=10, r=10, alpha=0.05, beta=0.05, g=200, x=40, y=450):
        """
         Конструктор класса мячей, которыми стреляет пушка
        :param colors: список возможных цветов мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        """
        Drawable.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = g
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.color = choice(colors)
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

    def remove_life(self):
        """
        Уменьшает время жизни мяча на 1
        """
        self.live -= 1

    def draw(self):
        """
        Рисует мяч на экране
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), int(self.r))

    def is_hit(self, target):
        """
        Проверяет, сталкивалкивается ли мяч с мишенью
        :param target: Мишень, с которой проверяется столкновение
        :return: True, если мяч сталкивается с мишенью, False иначе
        """
        return True if (self.x - target.x) ** 2 + (self.y - target.y) ** 2 < (self.r + target.r) ** 2 else False


class Gun(Drawable):
    def __init__(self, gun_color, charged_color, x=20, y=450, width=20, height=10, default_power=500):
        """
        Конструктор класса пушек
        :param gun_color: цвет пушки
        :param charged_color: цвет заряженной пушки
        :param x: координата центра вращения пушки по горизонтали
        :param y: координата центра вращения пушки по вертикали
        :param width: ширина пушки
        :param height: высота пушки
        :param power: скорость мяча, только что вылетевшего из пушки
        """
        Drawable.__init__(self)
        self.power = default_power
        self.is_active = False
        self.angle = 1
        self.color = gun_color
        self.gun_color = gun_color
        self.charged_color = charged_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.default_power = default_power

    def charge(self):
        """
        Заряжает пушку
        """
        self.is_active = True

    def fire(self, event, colors, lifetime=10, r=10, alpha=0.1, beta=0.0005, g=200):
        """
        Производит выстрел
        :param event: событие отпускания кнопки мыши
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :return: новый объект мяча
        """
        ball = self.new_ball(event, colors, lifetime, r, alpha, beta, g,
                             self.x + self.width * math.cos(self.angle), self.y + self.height * math.sin(self.angle))
        self.is_active = False
        self.power = self.default_power
        return ball

    def new_ball(self, event, colors, lifetime, r, alpha, beta, g, x, y):
        """
        Создаёт новый мяч после выстрела
        :param event: событие отпускания кнопки мыши
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        :return: новый объект мяча
        """
        new_ball = Ball(colors, lifetime, r, alpha, beta, g, x, y)
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.power * math.cos(self.angle)
        new_ball.vy = self.power * math.sin(self.angle)
        return new_ball

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

    def power_up(self, charge_per_second=500, max_power=2000):
        """
        Добавляет определённое значение к заряду пушки, если она уже заряжена и её заряд меньше максимально допустимого
        Необходимое значение рассчитывается для одного кадра
        :param max_power: максимально допустимый заряд пушки
        :param charge_per_second: заряд, который пушка получает за секунду
        """
        if self.is_active and self.power < max_power:
            self.power += charge_per_second / self.fps
        self.define_color()


class Target(Drawable):
    def __init__(self, color, min_radius=20, max_radius=50, min_x=600, max_x=780, min_y=300, max_y=550, health=1):
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
        Drawable.__init__(self)
        self.x = randint(min_x, max_x)
        self.y = randint(min_y, max_y)
        self.vx = 0
        self.vy = 0
        self.r = randint(min_radius, max_radius)
        self.color = color
        self.health = health

    def hit(self, damage=1):
        """
        Наносит цели урон
        :param damage: количество нанесённого урона
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self):
        """
        Рисует мишень
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        """
        Перемещает мишень по прошествии единицы времени, учитывая отражение от стенок
        """
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
