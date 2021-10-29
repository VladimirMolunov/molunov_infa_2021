import math
import pygame
from random import randint, choice

FPS = 60
width = 800
height = 600
charge_per_second = 500
max_power = 2000
min_radius = 20
max_radius = 50
min_x = 500
max_x = 750
min_y = 300
max_y = 550
health = 1
ball_lifetime = 10
r = 10
ball_alpha = 0.1
ball_beta = 0.0005
g = 200
gun_x = 20
gun_y = 450
gun_width = 20
gun_height = 10
gun_default_power = 500
max_target_x_speed = 300
max_target_y_speed = 300
border = 450
target_count = 2
score_for_catch = 1


class Drawable:
    def __init__(self, width=width, height=height, fps=FPS):
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


class Bullet(Drawable):
    def __init__(self, lifetime=ball_lifetime, alpha=ball_alpha, beta=ball_beta, g=g):
        """
        Конструктор класса снарядов
        :param lifetime: время жизни снаряда в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        """
        Drawable.__init__(self)
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.live = lifetime * self.fps

    def remove_life(self):
        """
        Уменьшает время жизни мяча на 1
        """
        self.live -= 1


class Weapon(Drawable):
    def __init__(self, x=gun_x, y=gun_y):
        """
        Конструктор класса стреляющих орудий
        :param x: координата центра вращения орудия по горизонтали
        :param y: координата центра вращения орудия по вертикали
        """
        Drawable.__init__(self)
        self.x = x
        self.y = y
        self.is_active = False
        self.angle = 1

    def charge(self):
        """
        Заряжает орудие
        """
        self.is_active = True


class Target(Drawable):
    def __init__(self, health):
        """
        Конструктор класса мишеней
        :param health: количество очков здоровья мишени
        """
        Drawable.__init__(self)
        self.health = health



class Ball(Bullet):
    def __init__(self, color, lifetime=ball_lifetime, r=r, x=0, y=0):
        """
         Конструктор класса мячей, которыми стреляет пушка
        :param color: цвет мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        """
        Bullet.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = self.g
        self.color = color
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


class Gun(Weapon):
    def __init__(self, gun_color, charged_color, width=gun_width, height=gun_height,
                 default_power=gun_default_power):
        """
        Конструктор класса пушек
        :param gun_color: цвет пушки
        :param charged_color: цвет заряженной пушки
        :param width: ширина пушки
        :param height: высота пушки
        :param default_power: скорость мяча, только что вылетевшего из пушки
        """
        Weapon.__init__(self)
        self.power = default_power
        self.color = gun_color
        self.gun_color = gun_color
        self.charged_color = charged_color
        self.width = width
        self.height = height
        self.default_power = default_power

    def fire_ball(self, event, colors, lifetime=ball_lifetime, r=r):
        """
        Производит выстрел
        :param event: событие отпускания кнопки мыши
        :param colors: возможные цвета мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :return: новый объект мяча
        """
        ball = self.new_ball(event, choice(colors), lifetime, r,
                             self.x + self.width * math.cos(self.angle), self.y + self.height * math.sin(self.angle))
        self.is_active = False
        self.power = self.default_power
        return ball

    def new_ball(self, event, color, lifetime, r, x, y):
        """
        Создаёт новый мяч после выстрела
        :param event: событие отпускания кнопки мыши
        :param color: цвет мяча
        :param lifetime: время жизни мяча в секундах
        :param r: радиус мяча
        :param x: начальная координата мяча по горизонтали
        :param y: начальная координата мяча по вертикали
        :return: новый объект мяча
        """
        new_ball = Ball(color, lifetime, r, x, y)
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

    def power_up(self, charge_per_second=charge_per_second, max_power=max_power):
        """
        Добавляет определённое значение к заряду пушки, если она уже заряжена и её заряд меньше максимально допустимого
        Необходимое значение рассчитывается для одного кадра
        :param max_power: максимально допустимый заряд пушки
        :param charge_per_second: заряд, который пушка получает за секунду
        """
        if self.is_active and self.power < max_power:
            self.power += charge_per_second / self.fps
        self.define_color()


class BallTarget(Target):
    def __init__(self, color, min_radius=min_radius, max_radius=max_radius, min_x=min_x, max_x=max_x, min_y=min_y,
                 max_y=max_y, health=health):
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
        Target.__init__(self, health)
        self.x = randint(min_x, max_x)
        self.y = randint(min_y, max_y)
        self.vx = randint(-1 * max_target_x_speed, max_target_x_speed)
        self.vy = randint(-1 * max_target_y_speed, max_target_y_speed)
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
        if self.r + border < self.x + self.vx / self.fps < self.screen_width - self.r:
            self.x += self.vx / self.fps
        else:
            self.vx = - self.vx
            self.x += self.vx / self.fps
        if self.r < self.y + self.vy / self.fps < self.screen_height - self.r:
            self.y += self.vy / self.fps
        else:
            self.vy = - self.vy
            self.y += self.vy / self.fps


class Game(Drawable):
    def __init__(self, target_color, background_color, gun_color, gun_charged_color, colors):
        Drawable.__init__(self)
        self.target_color = target_color
        self.background_color = background_color
        self.ball_colors = colors
        self.gun_color = gun_color
        self.gun_charged_color = gun_charged_color

    def main(self):
        score = 0
        target_list = []
        ball_list = []
        clock = pygame.time.Clock()
        gun = Gun(self.gun_color, self.gun_charged_color)
        for i in range(target_count):
            target_list.append(BallTarget(self.target_color))
        finished = False

        while not finished:
            self.screen.fill(self.background_color)
            gun.draw()
            for target_obj in target_list:
                target_obj.draw()
            for ball in ball_list:
                ball.draw()
            pygame.display.update()

            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gun.charge()
                elif event.type == pygame.MOUSEBUTTONUP:
                    ball_list.append(gun.fire_ball(event, self.ball_colors))
                elif event.type == pygame.MOUSEMOTION:
                    gun.targetting(event)

            for target in target_list:
                target.move()
            for ball in ball_list:
                ball.move()
                for target in target_list:
                    if ball.is_hit(target) and target.health > 0:
                        target.hit()
                        if target.health == 0:
                            target.__init__(self.target_color)
                            score += score_for_catch
                ball.remove_life()
                if ball.live <= 0:
                    ball_list.pop(0)
            gun.power_up()
        pygame.quit()
        return score
