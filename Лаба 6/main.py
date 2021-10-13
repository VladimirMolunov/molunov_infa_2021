import pygame
from pygame.draw import *
from random import randint
pygame.init()

# настраиваемые параметры
TPS = 60  # количество кадров в секунду
TicksPerBall = 30  # количество кадров, через которое появляется шарик
TicksPerAmogus = 50  # количество кадров, через которое может появиться мишень
chance = 5  # 1:chance - шанс появления мишени
(screen_width, screen_height) = (1200, 750)  # размеры экрана
score_for_ball = 1  # количество очков за клик по шарику
score_for_amogus = 10  # количество очков за клик по мишени
max_number_of_balls = 10  # максимальное количество шариков на экране, по достижении которого они начинают исчезать
max_number_of_amogus = 10  # максимальное количество мишеней на экране, по достижении которого они начинают исчезать
amogus_lifetime = 8  # время жизни мишени
max_radius = 100  # максимальный радиус шарика
max_speed = 320  # максимальная скорость шарика (в проекции на горизонтальную или вертикальную ось)
min_radius = 20  # минимальный радиус шарика
max_height = 200  # максимальная высота мишени  
min_height = 50  # минимальная высота мишени
min_amogus_speed = 240  # максимальная скорость мишени (в проекции на горизонтальную или вертикальную ось)
max_amogus_speed = 480  # минимальная скорость мишени (в проекции на горизонтальную или вертикальную ось)
gap = 25  # отступ от края окошка до границы игрового поля

# неизменяемые параметры
ratio = 19 / 50  # отношение роловины ширины мишени к её высоте
dt = float(1/TPS)  # время в секундах, которое проходит за 1 кадр
# объявление границ игрового поля
(leftborder, rightborder, topborder, bottomborder) = (gap, screen_width - gap, gap, screen_height - gap)
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0  # набранные очки

# объявление цветов шариков
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIME = (0, 255, 0)
GREEN = (30, 123, 30)
MAGENTA = (255, 0, 255)
VIOLET = (170, 0, 170)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, LIME, GREEN, MAGENTA, CYAN, ORANGE, VIOLET]

# объявление цветов мишеней
amogus_red = (RED, (170, 0, 0))
amogus_blue = (BLUE, (0, 0, 170))
amogus_white = (255, 255, 255)
amogus_gray = (170, 170, 170)
amogus_green = (GREEN, (20, 82, 20))
amogus_yellow = (YELLOW, (170, 170, 0))
amogus_orange = (ORANGE, (170, 85, 0))
amogus_black = ((60, 60, 60), (40, 40, 40))
amogus_cyan = (CYAN, (0, 170, 170))
amogus_pink = ((255, 105, 192), (170, 70, 128))
amogus_purple = ((105, 0, 128), (70, 0, 85))
amogus_brown = ((139, 69, 19), (93, 46, 13))
amogus_lime = (LIME, (0, 170, 0))

AMOGUS_COLORS = [amogus_red, amogus_blue, (amogus_white, amogus_gray), amogus_green, amogus_yellow, amogus_orange,
                 amogus_cyan, amogus_pink, amogus_purple, amogus_brown, amogus_lime, amogus_black]
(amogus_light, amogus_dark) = ((104, 226, 227), (40, 128, 129))

# объявление остальных цветов
transparent = (200, 200, 200, 0)
background = (0, 50, 80)
border = (0, 20, 40)


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
    :param color: кортеж цветов мишени
    :param surface: поверхность, на которой нарисована мишень
    :param timeleft: оставшееся время жизни мишени (в кадрах)
    """
    def __init__(self, initialised, status, faces_right, x, y, r, vx, vy, color, surface, timeleft):
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
        self.timeleft = timeleft

    def rotate(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

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
        if right_border - int(self.r * ratio) > (self.x + velx * time) > left_border + int(self.r * ratio):
            self.x += velx * time
        else:
            self.vx = -1 * self.vx
            velx = -1 * velx
            self.x += velx * time
            self.faces_right = True if (self.vx > 0) else False
            self.rotate()

        if bottom_border - int(self.r / 2) > (self.y + vely * time) > top_border + int(self.r / 2):
            self.y += vely * time
        else:
            self.vy = -1 * self.vy
            vely = -1 * vely
            self.y += vely * time


# объявление поверхностей рисования и их списков
ball_list = []
surface_list = []
for i in range(0, max_number_of_balls, 1):
    surface_list.append(pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA))
    surface_list[-1].fill(transparent)
    ball_list.append(Ball(False, True, 0, 0, 0, 0, 0, BLACK, surface_list[i]))

amogus_list = []
amogus_surface_list = []
for i in range(0, max_number_of_amogus, 1):
    amogus_surface_list.append(pygame.Surface((2 * max_height, 2 * max_height), pygame.SRCALPHA))
    amogus_surface_list[-1].fill(transparent)
    amogus_list.append(Amogus(False, True, True, 0, 0, 0, 0, 0, amogus_red, amogus_surface_list[i], 0))


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
    surface1 = pygame.Surface((280, 398), pygame.SRCALPHA)
    surface2 = pygame.Surface((500, 900), pygame.SRCALPHA)
    surface3 = pygame.Surface((280, 120), pygame.SRCALPHA)
    surface1.fill(transparent)
    rect(surface1, darkcolor, (15, 0, 250, 398))
    ellipse(surface2, lightcolor, (115, 115, 275, 478))
    surface2 = pygame.transform.rotate(surface2, -10)
    surface1.blit(surface2, (-222, -260))
    rect(surface1, transparent, (0, 0, 280, 70))
    rect(surface1, transparent, (0, 0, 15, 390))
    surface3.fill(transparent)
    ellipse(surface3, BLACK, (0, 0, 280, 240), 15)

    rect(surface, lightcolor, (50, 153, 315, 100), 0, -1, 0, 40, 0, 40)
    ellipse(surface, darkcolor, (180, 195, 240, 268))
    rect(surface, transparent, (0, 376, 380, 124))
    rect(surface, transparent, (365, 340, 15, 40))
    rect(surface, BLACK, (50, 153, 330, 238), 15, 40, 0, 40, 0, 40)
    ellipse(surface, lightcolor, (30, 0, 280, 240))
    ellipse(surface, darkcolor, (190, 360, 120, 140))
    rect(surface, BLACK, (190, 300, 120, 130))
    rect(surface, BLACK, (30, 350, 114, 64))
    rect(surface, BLACK, (30, 120, 280, 273))
    ellipse(surface, BLACK, (190, 360, 120, 140), 15)
    rect(surface, darkcolor, (206, 363, 89, 67))
    ellipse(surface, darkcolor, (30, 334, 114, 160))
    ellipse(surface, BLACK, (30, 334, 114, 160), 15)
    rect(surface, darkcolor, (45, 363, 84, 41))
    rect(surface, darkcolor, (45, 363, 250, 50))
    rect(surface, BLACK, (129, 398, 77, 15), 0, -1, 10, 10, 0, 0)
    surface.blit(surface1, (30, 0))
    surface.blit(surface3, (30, 0))
    ellipse(surface, amogus_dark, (0, 83, 230, 150))
    ellipse(surface, amogus_light, (25, 95, 150, 91))
    ellipse(surface, amogus_white, (45, 112, 100, 41))
    ellipse(surface, BLACK, (0, 83, 230, 150), 15)


def drawamogus(surface, color, height, right_orientation):
    """
    Рисует мишень заданного размера и возвращает поверхность с ней
    :param surface: поерхность для рисования мишени
    :param color: кортеж цветов мишени
    :param height: высота мишени
    :param right_orientation: ориентация по горизонтали: вправо - True, влево - False
    """
    draw_amogus(surface, color[0], color[1])
    if right_orientation:
        surface = pygame.transform.flip(surface, True, False)
    scaled_surface = pygame.transform.scale(surface, (int(height * ratio * 2), height))
    return scaled_surface


def new_amogus(amoguslist):
    """
    Рисует новую мишень со случайными координатами и высотой
    Добавляет его параметры в список amoguslist
    """
    global amogus_surface_list
    h = randint(min_height, max_height)
    x = randint(leftborder + int(ratio * h), rightborder - int(ratio * h))
    y = randint(topborder + int(h / 2), bottomborder - int(h / 2))
    vertical = randint(0, 1)
    horizontal = randint(0, 1)
    vx = randint(min_amogus_speed, max_amogus_speed)
    if horizontal == 1:
        vx = -1 * vx
    orientated_right = True if (vx > 0) else False
    vy = randint(min_amogus_speed, max_amogus_speed)
    if vertical == 1:
        vy = -1 * vy
    color = AMOGUS_COLORS[randint(0, len(AMOGUS_COLORS)) - 1]
    amogus_surface_list.pop(0)
    amogus_surface_list.append(pygame.Surface((380, 500), pygame.SRCALPHA))
    amoguslist.append(Amogus(True, True, orientated_right, x, y, h, vx, vy, color, amogus_surface_list[-1],
                             amogus_lifetime * TPS))
    amoguslist.pop(0)
    newamogus = amoguslist[-1]
    newamogus.surface.fill(transparent)
    newamogus.surface = drawamogus(newamogus.surface, newamogus.color, newamogus.r, newamogus.faces_right)


def inside_rect(position, x, y, w, h):
    """
    Проверяет попадание курсора внутрь прямоугольника
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты левого верхнего угла прямоугольника
    w - ширина прямоугольника
    h - высота прямоугольника
    """
    return True if ((x <= position[0] <= x + w) and (y <= position[1] <= y + h)) else False


def inside_circle(position, x, y, r):
    """
    Проверяет попадание курсора внутрь круга
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты центра круга
    r - радиус круга
    """
    return True if ((position[0] - x) ** 2 + (position[1] - y)**2 <= r ** 2) else False


def inside_rounded_rect(position, x, y, w, h, r):
    """
    Проверяет попадание курсора внутрь скругленного прямоугольника
    position - координаты клика (кортеж из 2 элементов - x и y)
    x, y - координаты левого верхнего угла прямоугольника
    w - ширина прямоугольника
    h - высота прямоугольника
    r - радиус скругления
    """
    return True if ((x + r <= position[0] <= x + w - 2 * r) and (y <= position[1] <= y + h))\
                   or ((x <= position[0] <= x + w) and (y + r <= position[1] <= y + h - 2 * r))\
                   or (inside_circle(position, x + r, y + r, r)) \
                   or (inside_circle(position, x + w - r, y + r, r)) \
                   or (inside_circle(position, x + r, y + h - r, r)) \
                   or (inside_circle(position, x + w - r, y + h - r, r)) else False


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


def inside_amogus(position, target):
    """
    Проверяет попадание точки с координатами position (кортеж из двух координат по x и y) внутрь данной мишени target
    """
    x = target.x - int(target.r * ratio)
    y = target.y - int(target.r / 2)
    scale = target.r / 500

    a1 = inside_ellipse(position, x + scale * 30, y, scale * 140, scale * 120)
    a2 = inside_ellipse(position, x, y + scale * 83, scale * 115, scale * 75)
    a3 = inside_rounded_rect(position, x + scale * 50, y + scale * 153, scale * 330, scale * 238, scale * 40)
    a4 = inside_ellipse(position, x + scale * 190, y + scale * 360, scale * 60, scale * 70)
    a5 = inside_ellipse(position, x + scale * 30, y + scale * 334, scale * 57, scale * 80)
    a6 = inside_rect(position, x + scale * 191, y + scale * 300, scale * 119, scale * 130)
    a7 = inside_rect(position, x + scale * 30, y + scale * 350, scale * 114, scale * 64)
    a8 = inside_rect(position, x + scale * 30, y + scale * 120, scale * 280, scale * 273)
    a9 = inside_rect(position, x + scale * 45, y + scale * 363, scale * 250, scale * 50)
    return True if a1 or a2 or a3 or a4 or a5 or a6 or a7 or a8 or a9 else False


pygame.display.update()
clock = pygame.time.Clock()
finished = False
tickcount = 0  # отсчёт количества кадров с момента запуска игры

while not finished:
    clock.tick(TPS)
    tickcount += 1
    screen.fill(border)
    rect(screen, background, (gap, gap, screen_width - 2 * gap, screen_height - 2 * gap))
    for ball in ball_list:
        if ball.status:
            ball.moveball(ball.vx, ball.vy, dt, leftborder, rightborder, topborder, bottomborder)
            screen.blit(ball.surface, (ball.x - max_radius, ball.y - max_radius))
    for amogus in amogus_list:
        if amogus.status:
            amogus.moveamogus(amogus.vx, amogus.vy, dt, leftborder, rightborder, topborder, bottomborder)
            screen.blit(amogus.surface, (amogus.x - int(amogus.r * ratio), amogus.y - int(amogus.r / 2)))
            amogus.timeleft -= 1
            if amogus.timeleft <= 0:
                amogus.status = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            captured = False
            for amogus in reversed(amogus_list):
                is_inside = inside_amogus(event.pos, amogus)
                if is_inside:
                    if amogus.status:
                        score += score_for_amogus
                        amogus.status = False
                        captured = True
                        break
            if not captured:
                for ball in reversed(ball_list):
                    is_inside = inside_circle(event.pos, ball.x, ball.y, ball.r)
                    if is_inside:
                        if ball.status:
                            score += score_for_ball
                            ball.status = False
                            break
    if tickcount % TicksPerBall == 0:
        if tickcount % TicksPerAmogus == 0:
            tickcount = 0
        else:
            new_ball(ball_list)
    if tickcount % TicksPerAmogus == 0:
        new = randint(0, chance - 1)
        if new == 0:
            new_amogus(amogus_list)
        else:
            if tickcount == 0:
                new_ball(ball_list)
    pygame.display.update()

pygame.quit()
print("Well done, your score is", score)
