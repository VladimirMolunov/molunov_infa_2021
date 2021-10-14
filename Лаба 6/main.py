import pygame
from random import randint
from mymodules import ballmod, amogusmod, inside, files
pygame.init()

# настраиваемые параметры
names = ('TPS', 'TicksPerBall', 'TicksPerAmogus', 'chance', 'screen_width', 'screen_height', 'score_for_ball',
         'score_for_amogus', 'max_number_of_balls', 'max_number_of_amogus', 'amogus_lifetime', 'max_radius',
         'max_speed', 'min_radius', 'max_height', 'min_height', 'min_amogus_speed', 'max_amogus_speed', 'gap')

# files.reset_custom()  # функция, позволяющая сбросить пользовательские настройки

files.getdefault(names)
if files.custom_path.exists():
    files.getcustom(names)
for j in names:
    exec(j + ' = files.' + j)

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
PURPLE = (105, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, LIME, GREEN, MAGENTA, CYAN, ORANGE, PURPLE]

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
amogus_purple = (PURPLE, (70, 0, 85))
amogus_brown = ((139, 69, 19), (93, 46, 13))
amogus_lime = (LIME, (0, 170, 0))

AMOGUS_COLORS = [amogus_red, amogus_blue, (amogus_white, amogus_gray), amogus_green, amogus_yellow, amogus_orange,
                 amogus_cyan, amogus_pink, amogus_purple, amogus_brown, amogus_lime, amogus_black]
(amogus_light, amogus_dark) = ((104, 226, 227), (40, 128, 129))

# объявление остальных цветов
transparent = (200, 200, 200, 0)
background = (0, 50, 80)
border = (0, 20, 40)

# переобозначение классов для простоты
Ball = ballmod.Ball
Amogus = amogusmod.Amogus

# объявление поверхностей рисования и их списков
ball_list = []
ballmod.defsurfacelist(max_number_of_balls, max_radius, transparent, ball_list)
amogus_list = []
amogusmod.defsurfacelist(max_number_of_amogus, max_height, transparent, amogus_list, Amogus, amogus_red)


# определение функций, извлечнных из соответствующих модулей, для заданных переменных
def new_ball(balllist):
    """
    Рисует новый шарик со случайными координатами и радиусом
    Добавляет его параметры в список balllist
    :param balllist: список шариков
    """
    ballmod.new_ball(balllist, min_radius, max_radius, leftborder, rightborder, topborder, bottomborder, max_speed,
                     COLORS, transparent)


def new_amogus(amoguslist):
    """
    Рисует новую мишень со случайными координатами и высотой
    Добавляет его параметры в список amoguslist
    :param amoguslist: список мишеней
    """
    amogusmod.new_amogus(amoguslist, min_height, max_height, leftborder, rightborder, topborder, bottomborder, ratio,
                         min_amogus_speed, max_amogus_speed, AMOGUS_COLORS, amogus_lifetime, TPS, transparent, BLACK,
                         amogus_dark, amogus_light, amogus_white)


def inside_amogus(position, target):
    """
    Проверяет попадание курсора в момент клика внутрь данной мишени
    :param position: позиция курсора в момент клика (кортеж из двух координат - по x и y)
    :param target: мишень (объект класса Amogus)
    :return: True, если точка клика попадает в мишень, False иначе
    """
    return inside.inside_amogus(position, target, ratio)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
tickcount = 0  # отсчёт количества кадров с момента запуска игры

while not finished:
    clock.tick(TPS)
    tickcount += 1
    screen.fill(border)
    pygame.draw.rect(screen, background, (gap, gap, screen_width - 2 * gap, screen_height - 2 * gap))
    for ball in ball_list:
        if ball.status:
            ball.moveball(ball.vx, ball.vy, dt, leftborder, rightborder, topborder, bottomborder)
            screen.blit(ball.surface, (ball.x - max_radius, ball.y - max_radius))
    for amogus in amogus_list:
        if amogus.status:
            amogus.moveamogus(amogus.vx, amogus.vy, dt, leftborder, rightborder, topborder, bottomborder, ratio)
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
                    is_inside = inside.inside_circle(event.pos, ball.x, ball.y, ball.r)
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
