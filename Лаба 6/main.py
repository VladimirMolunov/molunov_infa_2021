import pygame
from pygame.draw import *
from random import randint
pygame.init()

TPS = 30
TicksPerFrame = 15
screen = pygame.display.set_mode((1200, 900))
score = 0
(x, y, r) = (-2, -2, 0)
max_number_of_balls = 4

ball_list = []
for i in range(0, max_number_of_balls + 1, 1):
    ball_list.append([0] * 3)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball(balllist):
    """
    Рисует новый шарик со случайными координатами x, y и радиусом r
    Добавляет его параметры в список balllist
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    balllist.append([x, y, r])
    if balllist[max_number_of_balls] != (0, 0, 0):
        for j in (0, 1, 2):
            balllist.pop([0][j])


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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in ball_list:
                is_inside = inside(event.pos, x, y, r)
                if is_inside:
                    score += 1
    if tickcount % TicksPerFrame == 0:
        tickcount = 0
        new_ball(ball_list)
        pygame.display.update()
        screen.fill(BLACK)

pygame.quit()
print("Well done, your score is", score)
