import pygame
from pathlib import Path

from modules.classes import Showable, Background
from modules.buttons import ButtonGrid
from modules.vars import *

pygame.init()


class Menu(Showable):
    def __init__(self, grid: ButtonGrid, link_array: list, text, color, bg_filename, back=0, x=-1, y=-1, gap=30,
                 added_gap=30, line_gap=20, size=40, font='arial'):
        """
        Конструктор класса меню
        :param grid: столбец кнопок
        :param link_array: список номеров меню в общем списке, на которые ведут кнопки
        :param back: номер предыдущего меню в общем списке
        :param text: дополнительный текст меню
        :param color: цвет текста меню
        :param bg_filename: название файла с фоном
        :param x: координата центра текста по горизонтали
        :param y: координата центра текста по вертикали (если обе координаты не заданы, помещается под столбцом кнопок)
        :param gap: отступ от нижнего края столбца кнопок до текста
        :param added_gap: отступ от нижнего края текста до дополнительных изображений
        :param line_gap: отступ между строками текста
        :param size: размер текста меню
        :param font: шрифт текста меню
        """
        Showable.__init__(self)
        self.grid = grid
        self.text = text
        self.default_text = text
        self.x_inp = x
        self.y_inp = y
        self.x = 0
        self.y = 0
        self.color = color
        self.bg = Background(Path('images', bg_filename).resolve())
        self.link_array = link_array
        self.back = back
        self.font = font
        self.size = size
        self.gap = gap
        self.added_gap = added_gap
        self.line_gap = line_gap - self.size * 17/40
        self.text_surface = self.get_text()
        self.get_coords()
        self.added_images = []
        self.game = None

    def get_coords(self):
        """
        Задаёт координаты текста меню на экране
        """
        w = self.text_surface.get_width()
        h = self.text_surface.get_height()
        if self.x_inp == -1 and self.y_inp == -1:
            self.x = self.grid.x_center - w / 2
            self.y = self.grid.bottom() + self.gap
        else:
            self.x = self.x_inp - w / 2
            self.y = self.y_inp - h / 2

    def get_text(self):
        """
        Создаёт и возвращает поверхность с текстом
        """
        font = pygame.font.SysFont(self.font, self.size)
        text_list = []
        h = -self.line_gap
        w = 0
        txt = self.text.rsplit('\n')
        for line in txt:
            text_surface = font.render(line, True, self.color)
            text_list.append(text_surface)
            width = text_surface.get_width()
            height = text_surface.get_height()
            if width > w:
                w = width
            h += self.line_gap + height
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        h = 0
        for surf in text_list:
            width = surf.get_width()
            height = surf.get_height()
            surface.blit(surf, ((w - width) / 2, h))
            h += height + self.line_gap
        return surface

    def put_text(self):
        """
        Помещает текст меню на экран
        """
        self.screen.blit(self.text_surface, (self.x, self.y))

    def image_add(self, surface: pygame.Surface):
        """
        Добавляет дополнительное изображение под текстом в меню
        """
        self.added_images.append(surface)

    def image_blit(self, surface: pygame.Surface):
        """
        Выводит дополнительное изображение под текстом на экран
        """
        self.screen.blit(surface, ((self.screen_width - surface.get_width()) / 2,
                                   self.get_text_bottom() + self.added_gap))

    def blit(self):
        """
        Выводит меню на экран
        """
        self.bg.blit()
        self.grid.blit()
        self.put_text()
        for i in self.added_images:
            self.image_blit(i)

    def check(self, event):
        """
        Проверяет нажатие на какую-либо из кнопок меню
        :param event: событие pygame
        :return: номер нажатой кнопки по вертикали (самая верхняя - 1) или 0, если ни одна не нажата;
        -1 - кнопка возврата назад, -2 - кнопка возврата в главное меню
        """
        return self.grid.check(event)

    def goto(self, event):
        """
        Возвращает значение номера меню, к которому необходимо перейти после нажатия кнопки, а также
        True, если нужно перейти в другое меню или False, если нужно остаться
        :param event: событие pygame (нажатие кнопки)
        """
        index = 0
        num = self.check(event)
        if num == 0:
            index = -1
        elif num == -1:
            index = self.back
        elif num == -2:
            index = 0
        elif num > 0:
            index = self.link_array[num - 1]
        return index

    def set_text(self, new_text: str):
        """
        Задаёт новый текст для меню
        :param new_text: новый текст
        """
        self.text = new_text
        self.text_surface = self.get_text()
        self.get_coords()

    def add_text(self, added_text: str):
        """
        Добавляет текст в меню с новой строки
        :param added_text: добавленный текст
        """
        self.text = self.default_text + ('\n' + added_text)
        self.text_surface = self.get_text()
        self.get_coords()

    def get_text_bottom(self):
        """
        Возвращает нижнюю координату текста по вертикали
        """
        return self.x + self.text_surface.get_height()


class GameMenu(Menu):
    def __init__(self, grid: ButtonGrid, link_array: list, text, color, bg_filename, back=0, x=-1, y=-1, gap=30,
                 game=None):
        """
        Конструктор класса игровых меню
        :param game: название игры, происходящей в меню
        """
        Menu.__init__(self, grid, link_array, text, color, bg_filename, back, x, y, gap)
        self.game = game
