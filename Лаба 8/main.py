import math
import numpy as np
from random import choice, randint
import pygame

FPS = 30
dt = 1 / FPS
power = 450
lifetime = 10
g = 200
radius = 15
a = 1
b = 1

transparent = (200, 200, 200, 0)
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = g
        self.color = choice(GAME_COLORS)
        self.live = lifetime * FPS

    def move(self, width, height):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.ax = - a * self.vx - b * self.vx ** 2
        self.ay = g + a * self.vy + b * self.vy ** 2
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        if self.r < self.x + self.vx * dt < width - self.r:
            self.x += self.vx * dt
        else:
            self.vx = - self.vx
            self.x += self.vx * dt
        if self.r < self.y + self.vy * dt < height - self.r:
            self.y += self.vy * dt
        else:
            self.vy = - self.vy
            self.y += self.vy * dt

    def remove_life(self):
        self.live -= 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.r))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return True if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2 else False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = power
        self.f2_on = False
        self.angle = 1
        self.color = GREY
        self.x = 20
        self.y = 450
        self.width = 20
        self.height = 10

    def fire2_start(self, event):
        self.f2_on = True

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r = radius
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls.append(new_ball)
        self.f2_on = False
        self.f2_power = power

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] == self.x:
                if event.pos[1] > self.y:
                    self.angle = np.pi / 2
                else:
                    self.angle = - np.pi / 2
            else:
                self.angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        self.define_color()

    def define_color(self):
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x1 = self.x + self.height * math.sin(self.angle)
        x2 = self.x - self.height * math.sin(self.angle)
        x3 = self.x - self.height * math.sin(self.angle) + 2 * self.width * math.cos(self.angle)
        x4 = self.x + self.height * math.sin(self.angle) + 2 * self.width * math.cos(self.angle)
        y1 = self.y - self.height * math.cos(self.angle)
        y2 = self.y + self.height * math.cos(self.angle)
        y3 = self.y + self.height * math.cos(self.angle) + 2 * self.width * math.sin(self.angle)
        y4 = self.y - self.height * math.cos(self.angle) + 2 * self.width * math.sin(self.angle)
        pygame.draw.polygon(screen, self.color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
        self.define_color()


class Target:
    def __init__(self, target_screen):
        self.points = 0
        self.screen = target_screen
        self.live = True
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.color = RED
        self.init_target()

    def init_target(self):
        """ Инициализация новой цели. """
        global target_list
        target_list.append(self)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


def new_target(caught=0):
    """ Инициализация новой цели. """
    target_list.pop(caught)
    Target(screen)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
target_list = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in target_list:
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move(WIDTH, HEIGHT)
        for target in target_list:
            if b.hittest(target) and target.live:
                target.live = False
                target.hit()
                new_target(target_list.index(target))
            b.remove_life()
        if b.live <= 0:
            balls.pop(0)
    gun.power_up()

pygame.quit()
