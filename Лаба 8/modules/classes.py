import pygame

from modules.groups import bg, bullet_group, target_group

FPS = 60
width = 800
height = 600
g = 200


class DrawablesList(list):
    def __init__(self):
        """
        Конструктор класса списков объектов типа Drawable
        """
        list.__init__(self)

    def smart_pop(self, index=-1):
        """
        Убирает объект класса Drawable из соответствующего списка и удаляет его спраайт из всех групп
        :param index: номер элемента, который необходимо убрать, в списке
        """
        self[index].sprite.kill()
        self.pop(index)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса спрайтов
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(0, 0))


class Showable:
    def __init__(self, width=width, height=height, fps=FPS):
        """
        Конструктор класса объектов, связанных с выводом изображения на экран
        :param width: ширина экрана
        :param height: высота экрана
        :param fps: частота обновления экрана в кадрах в секунду
        """
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.screen_width = width
        self.screen_height = height


class Background(Showable):
    def __init__(self, image):
        """
        Конструктор класса фоновых изображений
        :param image: путь к фоновой картинке
        """
        Showable.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.pos = (0, 0)
        self.config_image(image)

    def config_image(self, image):
        """
        Получает фоновое изображение
        :param image: путь к фоновой картинке
        """
        self.image = pygame.image.load(image)
        w = self.image.get_width() / self.screen_width
        h = self.image.get_height() / self.screen_height
        if w < h:
            h = int(h * self.screen_height / w)
            w = self.screen_width
            self.pos = (0, (self.screen_height - h) / 2)
        else:
            w = int(w * self.screen_width / h)
            h = self.screen_height
            self.pos = ((self.screen_width - w) / 2, 0)
        self.image = pygame.transform.scale(self.image, (w, h))

    def blit(self):
        """
        Рисует фон
        """
        self.screen.blit(self.image, self.pos)


class Drawable(Showable):
    def __init__(self, x=0, y=0):
        """
        Конструктор класса объектов игры, изображаемых на экране
        :param x: начальная координата центра объекта по горизонтали
        :param y: начальная координата центра объекта по вертикали
        """
        Showable.__init__(self)
        self.x = x
        self.y = y
        self.sprite = Sprite()

    def draw(self):
        """
        Рисует объект на поверхности и возвращает эту поверхность
        :return: объект типа pygame.Surface
        """
        return pygame.Surface((0, 0))

    def config_sprite(self):
        """
        Создаёт спрайт с данным объектом и получает его маску
        """
        self.sprite.image = self.draw()
        self.sprite.rect = self.sprite.image.get_rect(center=(self.x, self.y))

    def move_object(self):
        """
        Шаблон метода движения объекта
        """
        pass

    def move(self):
        """
        Двигает объект и обновляет его спрайт
        """
        self.move_object()
        self.config_sprite()


class Bullet(Drawable):
    def __init__(self, lifetime, alpha, beta, x=0, y=0, g=g):
        """
        Конструктор класса снарядов
        :param lifetime: время жизни снаряда в секундах
        :param alpha: параметр a в формуле силы трения F = -av - bv^2
        :param beta: параметр b в формуле силы трения F = -av - bv^2
        :param g: ускорение свободного падения
        :param x: начальная координата центра снаряда по горизонтали
        :param y: начальная координата центра снаряда по вертикали
        """
        Drawable.__init__(self, x, y)
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.live = lifetime * self.fps
        bullet_group.add(self.sprite)

    def remove_life(self):
        """
        Уменьшает время жизни мяча на 1
        """
        self.live -= 1

    def is_hit(self, target):
        """
        Проверяет, сталкивалкивается ли снаряд с мишенью
        :param target: Мишень, с которой проверяется столкновение
        :return: True, если снаряд сталкивается с мишенью, False иначе
        """
        return True if pygame.sprite.collide_mask(self.sprite, target.sprite) else False


class Target(Drawable):
    def __init__(self, health, border, x=0, y=0):
        """
        Конструктор класса мишеней
        :param health: количество очков здоровья мишени
        :param border: граница области по горизонтали, которую не может пересекать снаряд
        :param x: начальная координата центра мишени по горизонтали
        :param y: начальная координата центра мишени по вертикали
        """
        Drawable.__init__(self, x, y)
        self.health = health
        target_group.add(self.sprite)
        self.border = border
