import pygame
from pygame.draw import *
from random import randint
pygame.init()

TPS = 30
dt = float(1/TPS)
TicksPerBall = 15
(screen_width, screen_height) = (1200, 750)
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0
max_number_of_balls = 12
max_radius = 100
max_speed = 320
min_radius = 10
gap = 25
(leftborder, rightborder, topborder, bottomborder) = (gap, screen_width - gap, gap, screen_height - gap)


class Ball:
    """
    Класс шариков
    :param initialised: определяет, создан ли уже этот шарик (True) или объект является "пустышкой" (False)
    :param status: определяет, должен ли шарик быть видим на экране
    :param x: координата центра шарика по горизонтали
    :param y: координата центра шарика по вертикали
    :param r: радиус шарика
    :param vx: скорость шарика по горизонтали
    :param vy: скорость шарика по вертикали
    :param color: цвет шарика
    :param surface: поверхность, на которой нарисован шарик
    """
    def __init__(self, initialised, status, x, y, r, vx, vy, color, surface):
        self.initialised = initialised
        self.status = status
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.surface = surface

    def moveball(self, velx, vely, time, left_border, right_border, top_border, bottom_border):
        """
        Двигает шарик в соответствии с заданной скоростью
        velx - скорость по x в секунду
        vely - скорость по y в секунду
        time - время одного обновления экрана
        При необходимости осуществляет отражение шарика от стенок с координатами:
        left_border (координата x левой границы), right_border (координата x правой границы),
        top_border (координата y верхней границы), bottom_border (координата y нижней границы).
        """
        if right_border - self.r > (self.x + velx * time) > left_border + self.r:
            self.x += velx * time
        else:
            self.vx = -1 * self.vx
            velx = -1 * velx
            self.x += velx * time

        if bottom_border - self.r > (self.y + vely * time) > top_border + self.r:
            self.y += vely * time
        else:
            self.vy = -1 * self.vy
            vely = -1 * vely
            self.y += vely * time


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
transparent = (200, 200, 200, 0)
background = (0, 50, 80)
border = (0, 20, 40)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

ball_list = []
surface_list = []
for i in range(0, max_number_of_balls + 1, 1):
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    surface_list[-1].fill(transparent)
    ball_list.append(Ball(False, True, 0, 0, 0, 0, 0, BLACK, surface_list[i]))


def new_ball(balllist):
    """
    Рисует новый шарик со случайными координатами и радиусом
    Добавляет его параметры в список balllist
    """
    global surface_list
    r = randint(min_radius, max_radius)
    x = randint(leftborder + r, rightborder - r)
    y = randint(topborder + r, bottomborder - r)
    vx = randint(-1 * max_speed, max_speed)
    vy = randint(-1 * max_speed, max_speed)
    color = COLORS[randint(0, 5)]
    surface_list.pop(0)
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    balllist.append(Ball(True, True, x, y, r, vx, vy, color, surface_list[-1]))
    balllist.pop(0)
    newball = balllist[-1]
    newball.surface.fill(transparent)
    circle(newball.surface, newball.color, (max_radius, max_radius), newball.r)


def inside(position, x, y, r):
    """
    Проверяет попадание курсора внутрь шарика
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты центра шарика
    r - радиус шарика
    """
    return True if ((position[0] - x) ** 2 + (position[1] - y)**2 <= r ** 2) else False


pygame.display.update()
clock = pygame.time.Clock()
finished = False
tickcount = 0

while not finished:
    clock.tick(TPS)
    tickcount += 1
    screen.fill(border)
    rect(screen, background, (gap, gap, screen_width - 2 * gap, screen_height - 2 * gap))
    for ball in ball_list:
        ball.moveball(ball.vx, ball.vy, dt, leftborder, rightborder, topborder, bottomborder)
        if ball.status is True:
            screen.blit(ball.surface, (ball.x - max_radius, ball.y - max_radius))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in reversed(ball_list):
                is_inside = inside(event.pos, ball.x, ball.y, ball.r)
                if is_inside:
                    if ball.status:
                        score += 1
                        ball.status = False
                        break
    if tickcount % TicksPerBall == 0:
        tickcount = 0
        new_ball(ball_list)
    pygame.display.update()

pygame.quit()
print("Well done, your score is", score)
