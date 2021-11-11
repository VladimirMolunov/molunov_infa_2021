import pygame
from pathlib import Path

from modules.classes import Showable
from modules.menu import Menu
from modules.vars import *

pygame.init()


class Counter(Showable):
    def __init__(self, image, x=0, y=0, width=None, height=40, number=0,
                 font=None, fontsize=80, text_color=counter_color, left_gap=10, right_gap=10):
        """
        Конструктор класса счётчиков некоторых объектов

        :param image: иконка объекта, который он считает
        :param x: координата центра иконки на экране по горизонтали
        :param y: координата центра иконки на экране по вертикали
        :param height: высота иконки
        :param width: ширина иконки (None - сохранить пропорции картинки)
        :param number: количество объектов
        :param font: шрифт, которым отображается число
        :param fontsize: размер шрифта
        :param text_color: цвет текста
        :param left_gap: отступ от иконки до "крестика"
        :param right_gap: отступ от "крестика" до числа
        """
        Showable.__init__(self)
        self.image = image
        self.number = number
        self.def_x = x
        self.def_y = y
        self.x = 0
        self.y = 0
        self.height = height
        self.font = font
        self.text_color = text_color
        self.fontsize = fontsize
        self.left_gap = left_gap
        self.right_gap = right_gap
        if width is None:
            self.width = height * image.get_width() / image.get_height()
        else:
            self.width = width

    def add(self):
        """
        Добавляет 1 к количеству
        """
        self.number += 1

    def subtract(self):
        """
        Вычитает 1 из количества, обнуляет его в случае получения отрицательного значения
        """
        self.number -= 1
        if self.number < 0:
            self.number = 0

    def change_number(self, value):
        """
        Меняет количество
        :param value: новое значени количества
        :return:
        """
        self.number = value

    def draw(self):
        """
        Рисует счётчик, возвращает поверхность с ним
        Определяет координаты центра этой поверхности
        :return: объект типа pygame.Surface
        """
        surface1 = pygame.transform.scale(self.image, (int(self.width), int(self.height))).convert_alpha()
        surface1.set_colorkey(make_transparent)
        font = pygame.font.SysFont(self.font, self.fontsize)
        text = font.render(str(self.number), True, self.text_color)
        w = text.get_width()
        h = text.get_height()
        x = font.render('x', True, self.text_color)
        wx = x.get_width()
        hx = x.get_height()
        width = self.width + w + wx + self.left_gap + self.right_gap
        height = self.height
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(transparent)
        surface.blit(surface1, (0, 0))
        surface.blit(x, (self.width + self.left_gap, (self.height - hx) / 2))
        surface.blit(text, (self.width + self.left_gap + wx + self.right_gap, (self.height - h) / 2))
        self.x = self.def_x + (w + wx + self.left_gap + self.right_gap) / 2
        self.y = self.def_y
        return surface

    def blit(self):
        """
        Выводит счётчик на экран
        """
        s = self.draw()
        self.screen.blit(s, (self.x - s.get_width() / 2, self.y - s.get_height() / 2))


class TrophyScreen(Showable):
    def __init__(self, hare_skin_count=None, horns_count=None, bird_count=None, height=100, gap=20):
        """
        Конструктор класса полоски с количеством полученных трофеев, отображаемой на финальном экране игры "Охота"

        :param hare_skin_count: количество заячьих шкурок
        :param horns_count: количество оленьих рогов
        :param bird_count: количество птиц
        :param height: высота иконок трофеев в полоске
        :param gap: отступ между изображениями в полоске
        """
        Showable.__init__(self)
        self.hare_skin_count = hare_skin_count
        self.horns_count = horns_count
        self.bird_count = bird_count
        self.height = height
        self.gap = gap
        self.array = self.config_array()

    def config_array(self):
        """
        Создаёт список счётчиков, находящихся в полоске
        :return: список объектов класса Counter
        """
        array = []
        if self.hare_skin_count is not None:
            array.append(Counter(hare_skin, height=self.height, number=self.hare_skin_count))
        if self.horns_count is not None:
            array.append(Counter(horns, height=self.height, number=self.horns_count))
        if self.bird_count is not None:
            array.append(Counter(bird, height=self.height, number=self.bird_count))
        return array

    def draw(self):
        """
        Рисует полоску трофеев, возвращает поверхность с ней
        :return: объект типа pygame.Surface
        """
        (w, h) = (-self.gap, 0)
        for i in self.array:
            w += i.draw().get_width() + self.gap
            h_new = i.draw().get_height()
            if h < h_new:
                h = h_new
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        w = 0
        for i in self.array:
            s = i.draw()
            surface.blit(s, (w, (h - s.get_height()) / 2))
            w += s.get_width() + self.gap
        return surface

    def to_menu(self, menu: Menu):
        """
        Помещает полоску трофеев в меню
        :param menu: меню, в которое нужно поместить полоску
        """
        menu.image_add(self.draw())
