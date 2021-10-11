import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 0.5
screen = pygame.display.set_mode((1200, 900))
score = 0
(x, y, r) = (0, 0, 0)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """рисует новый шарик"""
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


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

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_inside = inside(event.pos, x, y, r)
            if is_inside:
                score += 1
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
print("Well done, your score is", score)
