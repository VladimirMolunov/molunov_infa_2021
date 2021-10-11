import pygame
from pygame.draw import *
from random import randint
pygame.init()

TPS = 30
dt = float(1/TPS)
TicksPerFrame = 15
screen = pygame.display.set_mode((1200, 900))
score = 0
(x, y, r) = (-2, -2, 0)
max_number_of_balls = 4


class Ball:
    def __init__(self, initialised, status, x, y, r, vx, vy, color):
        self.status = status
        self.initialised = initialised
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color

    def moveball(self, velx, vely, dt):
        """
        Двигает шарик
        :param velx: скорость по x в секунду
        :param vely: скорость по y в секунду
        :param dt: FPS экрана
        """
        self.x += velx * dt
        self.y += vely * dt


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

ball_list = []
for i in range(0, max_number_of_balls + 1, 1):
    ball_list.append(Ball(False, True, 0, 0, 0, 0, 0, BLACK))  # x, y, радиус, скорость x, скорость y


def new_ball(balllist):
    """
    Рисует новый шарик со случайными координатами x, y и радиусом r
    Добавляет его параметры в список balllist
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    vx = randint(10, 100)
    vy = randint(10, 100)
    color = COLORS[randint(0, 5)]
    balllist.append(Ball(True, True, x, y, r, vx, vy, color))
    balllist.pop(0)


def inside(position, x, y, r):
    """
    Проверяет попадание курсора внутрь шарика
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты центра шарика
    r - радиус шарика
    """
    return True if ((position[0]-x)**2 + (position[1]-y)**2 <= r**2) else False


pygame.display.update()
clock = pygame.time.Clock()
finished = False
tickcount = 0

while not finished:
    clock.tick(TPS)
    tickcount += 1
    for ball in ball_list:
        circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.r))
        ball.moveball(ball.vx, ball.vy, dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in ball_list:
                is_inside = inside(event.pos, ball.x, ball.y, ball.r)
                if is_inside:
                    if ball.status is True:
                        score += 1
                        ball.status = False
    if tickcount % TicksPerFrame == 0:
        tickcount = 0
        new_ball(ball_list)
    pygame.display.update()

pygame.quit()
print("Well done, your score is", score)
