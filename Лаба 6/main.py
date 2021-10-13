import pygame
from pygame.draw import *
from random import randint
pygame.init()

TPS = 30
dt = float(1/TPS)
TicksPerBall = 15
TicksPerAmogus = 50
chance = 3
(screen_width, screen_height) = (1200, 750)
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0
score_for_ball = 1
score_for_amogus = 10
max_number_of_balls = 12
max_number_of_amogus = 2
max_radius = 100
max_speed = 320
min_radius = 10
max_height = 200
min_height = 50
max_amogus_speed = 480
ratio = 19 / 50
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


class Amogus:
    """
    Другой тип мишеней
    :param initialised: определяет, создана ли уже эта мишень (True) или объект является "пустышкой" (False)
    :param status: определяет, должна ли мишень быть видима на экране
    :param faces_right: определяет ориентацию мишени по горизонтали: вправо - True, влево - False
    :param x: координата центра мишени по горизонтали
    :param y: координата центра мишени по вертикали
    :param r: высота мишени
    :param vx: скорость мишени по горизонтали
    :param vy: скорость мишени по вертикали
    :param color: цвет мишени
    :param surface: поверхность, на которой нарисована мишень
    """
    def __init__(self, initialised, status, faces_right, x, y, r, vx, vy, color, surface):
        self.initialised = initialised
        self.status = status
        self.faces_right = faces_right
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.surface = surface

    def moveamogus(self, velx, vely, time, left_border, right_border, top_border, bottom_border):
        """
        Двигает мишень в соответствии с заданной скоростью
        velx - скорость по x в секунду
        vely - скорость по y в секунду
        time - время одного обновления экрана
        При необходимости осуществляет отражение мишени от стенок с координатами:
        left_border (координата x левой границы), right_border (координата x правой границы),
        top_border (координата y верхней границы), bottom_border (координата y нижней границы).
        """
        if right_border - self.r > (self.x + velx * time) > left_border + self.r:
            self.x += velx * time
        else:
            self.vx = -1 * self.vx
            velx = -1 * velx
            self.x += velx * time
            self.faces_right = True if (self.vx > 0) else False

        if bottom_border - self.r > (self.y + vely * time) > top_border + self.r:
            self.y += vely * time
        else:
            self.vy = -1 * self.vy
            vely = -1 * vely
            self.y += vely * time


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIME = (0, 255, 0)
GREEN = (0, 170, 60)
MAGENTA = (255, 0, 255)
VIOLET = (170, 0, 170)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)
BLACK = (0, 0, 0)
transparent = (200, 200, 200, 0)
background = (0, 50, 80)
border = (0, 20, 40)
COLORS = [RED, BLUE, YELLOW, LIME, GREEN, MAGENTA, CYAN, ORANGE, VIOLET]

amogus_red = ((255, 0, 0), (170, 0, 0))
amogus_blue = ((0, 0, 255), (0, 0, 170))
amogus_white = (255, 255, 255)
amogus_gray = (170, 170, 170)
amogus_green = ((0, 255, 0), (0, 170, 0))
amogus_yellow = ((255, 255, 0), (170, 170, 0))
amogus_orange = ((255, 128, 0), (170, 85, 0))
AMOGUS_COLORS = [amogus_red, amogus_blue, (amogus_white, amogus_gray), amogus_green, amogus_yellow, amogus_orange]
(amogus_light, amogus_dark) = ((104, 226, 227), (40, 128, 129))

ball_list = []
surface_list = []
for i in range(0, max_number_of_balls + 1, 1):
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    surface_list[-1].fill(transparent)
    ball_list.append(Ball(False, True, 0, 0, 0, 0, 0, BLACK, surface_list[i]))

amogus_list = []
amogus_surface_list = []
for i in range(0, max_number_of_amogus + 1, 1):
    amogus_surface_list.append(pygame.Surface((2 * max_height, 2 * max_height), pygame.SRCALPHA))
    amogus_surface_list[-1].fill(transparent)
    amogus_list.append(Amogus(False, True, True, 0, 0, 0, 0, 0, BLACK, amogus_surface_list[i]))


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
    color = COLORS[randint(0, len(COLORS)) - 1]
    surface_list.pop(0)
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    balllist.append(Ball(True, True, x, y, r, vx, vy, color, surface_list[-1]))
    balllist.pop(0)
    newball = balllist[-1]
    newball.surface.fill(transparent)
    circle(newball.surface, newball.color, (max_radius, max_radius), newball.r)


def draw_amogus(surface, lightcolor, darkcolor):
    """
    Рисует мишень стандартного размера
    :param surface: поерхность для рисования мишени размера 380x500 пикселей
    :param lightcolor: основной цвет
    :param darkcolor: цвет тени
    """
    pass


def drawamogus(surface, color, height, right_orientation):
    """
    Рисует мишень заданного размера
    :param surface: поерхность для рисования мишени
    :param color: кортеж цветов мишени
    :param height: высота мишени
    :param right_orientation: ориентация по горизонтали: вправо - True, влево - False
    """
    draw_amogus(surface, color[0], color[1])
    if right_orientation:
        surface = pygame.transform.flip(surface, True, False)
    surface = pygame.transform.scale(surface, (int(height * ratio * 2), height))


def new_amogus(amoguslist):
    """
    Рисует новую мишень со случайными координатами и высотой
    Добавляет его параметры в список amoguslist
    """
    global amogus_list
    h = randint(min_height, max_height)
    x = randint(leftborder + int(ratio * h), rightborder - int(ratio * h))
    y = randint(topborder + int(h / 2), bottomborder - int(h / 2))
    vx = randint(-1 * max_amogus_speed, max_amogus_speed)
    orientated_right = True if (vx > 0) else False
    vy = randint(-1 * max_amogus_speed, max_amogus_speed)
    color = AMOGUS_COLORS[randint(0, len(AMOGUS_COLORS)) - 1]
    amogus_surface_list.pop(0)
    amogus_surface_list.append(pygame.Surface((380, 500), pygame.SRCALPHA))
    amoguslist.append(Amogus(True, True, orientated_right, x, y, h, vx, vy, color, amogus_surface_list[-1]))
    amoguslist.pop(0)
    newamogus = amoguslist[-1]
    newamogus.surface.fill(transparent)
    drawamogus(newamogus.surface, newamogus.color, newamogus.r, newamogus.faces_right)


def inside_rect(position, x, y, w, h):
    """
    Проверяет попадание курсора внутрь прямоугольника
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты левого верхнего угла прямоугольника
    w - ширина прямоугольника
    h - высота прямоугольника
    """
    return True if ((x <= position[0] <= x+w) and (y <= position[1] <= y+h)) else False


def inside_ellipse(position, x, y, half_w, half_h):
    """
    Проверяет попадание курсора внутрь эллипса
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты левого верхнего угла прямоугольника, задающего эллипс
    w - половина ширины эллипса
    h - половина высоты эллипса
    """
    return True if (half_h ** 2 * (position[0] - x - half_w) ** 2 + half_w ** 2 * (position[1] - y - half_h) ** 2 <=
                    (half_w * half_h) ** 2) else False


def inside_circle(position, x, y, r):
    """
    Проверяет попадание курсора внутрь круга
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты центра круга
    r - радиус круга
    """
    return True if ((position[0] - x) ** 2 + (position[1] - y)**2 <= r ** 2) else False


def inside_amogus(amogus):
    """
    Проверяет попадание курсора внутрь данной мишени
    """
    return False


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
    for amogus in amogus_list:
        amogus.moveamogus(amogus.vx, amogus.vy, dt, leftborder, rightborder, topborder, bottomborder)
        if amogus.status is True:
            screen.blit(amogus.surface, (int(max_height * ratio), int(max_height / 2)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in reversed(ball_list):
                is_inside = inside_circle(event.pos, ball.x, ball.y, ball.r)
                if is_inside:
                    if ball.status:
                        score += score_for_ball
                        ball.status = False
                        break
            for amogus in reversed(amogus_list):
                is_inside = inside_amogus(amogus)
                if is_inside:
                    if amogus.status:
                        score += score_for_amogus
                        amogus.status = False
                        break
    if tickcount % TicksPerBall == 0:
        tickcount = 0
        new_ball(ball_list)

    pygame.display.update()

pygame.quit()
print("Well done, your score is", score)
