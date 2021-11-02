import pygame
from pathlib import Path

from modules.classes import Drawable, Showable, Background

pygame.init()
make_transparent = (255, 255, 255)
screen = pygame.display.set_mode((800, 600))
def_image = pygame.image.load(Path('images', 'def_button.png').resolve()).convert_alpha()
image_pressed = pygame.image.load(Path('images', 'pressed_button.png').resolve()).convert_alpha()
image_pointed = pygame.image.load(Path('images', 'pointed_button.png').resolve()).convert_alpha()


class Button:
    def __init__(self, x, y, text, text_color):
        """
        Конструктор класса кнопок
        :param x: координата центра кнопки по горизонтали
        :param y: координата центра кнопки по вертикали
        :param text: текст на кнопке
        :param text_color: цвет текста на кнопке
        """
        self.image = def_image
        self.image_pointed = image_pointed
        self.image_pressed = image_pressed
        for i in (self.image, self.image_pressed, self.image_pointed):
            i.set_colorkey(make_transparent)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.render = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render.blit(self.image, (0, 0))
        self.text = text
        self.text_color = text_color
        self.x = x
        self.y = y
        self.is_pressed = False
        self.is_pointed = False

    def check_press(self, event: pygame.event.Event):
        """
        Проверяет нажатие или отпускание кнопки
        :param event: событие нажатия/отпускания кнопки мыши
        :return: True, если кнопка нажата, иначе False
        """
        checked = False
        if self.is_pointed:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.is_pressed:
                    checked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (-1 * self.width / 2 < event.pos[0] - self.x < self.width / 2) and\
                        (-1 * self.height / 2 < event.pos[1] - self.y < self.height / 2):
                    self.is_pressed = True
        else:
            self.is_pressed = False
        return checked

    def check_pointed(self, event: pygame.event.Event):
        """
        Проверяет наведение курсора на кнопку
        :param event: событие движения кнопки мыши
        """
        if event.type == pygame.MOUSEMOTION:
            if (-1 * self.width / 2 < event.pos[0] - self.x < self.width / 2) and\
                    (-1 * self.height / 2 < event.pos[1] - self.y < self.height / 2):
                self.is_pointed = True
            else:
                self.is_pointed = False

    def put_text(self):
        """
        Помещает текст на изображения кнопки
        """
        font = pygame.font.SysFont('dejavuserif', int(0.56 * self.height))
        text = font.render(self.text, True, self.text_color)
        w = text.get_width()
        h = text.get_height()
        self.render.blit(text, (self.width / 2 - w / 2, self.height / 2 - h / 2))

    def set_image(self):
        """
        Задаёт нужное изображение кнопки
        """
        if self.is_pressed:
            self.render.fill(make_transparent)
            self.render.blit(self.image_pressed, (0, 0))
        else:
            if self.is_pointed:
                self.render.fill(make_transparent)
                self.render.blit(self.image_pointed, (0, 0))
            else:
                self.render.fill(make_transparent)
                self.render.blit(self.image, (0, 0))
        self.render.set_colorkey(make_transparent)

    def check(self, event):
        """
        Проверяет нажатие и наведение курсора на кнопку
        :param event: событие pygame
        :return: True, если кнопка нажата, иначе False
        """
        self.check_pointed(event)
        return self.check_press(event)

    def blit(self, surface: pygame.Surface):
        """
        Рисует кнопку
        :param surface: поверхность рисования
        """
        self.set_image()
        self.put_text()
        surface.blit(self.render, (self.x - self.width / 2, self.y - self.height / 2))

    def set_y(self, value):
        """
        Переопределяет значение координаты центра кнопки по вертикали
        :param value: новое значение координаты
        """
        self.y = value


class ButtonGrid(Showable):
    def __init__(self, color, x_center, y_top, button_text_array: list, main=False, back=False, gap=10, big_gap=30):
        """
        Вертикальный столбец из кнопок
        :param color: цвет кнопок в столбце
        :param x_center: координата центра столбца по горизонтали
        :param y_top: координата верхнего края столбца по вертикали
        :param button_text_array: список текстов на кнопках
        :param main: определяет, есть ли кнопка выхода в главное меню
        :param back: определяет, есть ли кнопка возврата назад
        :param gap: отступ между кнопками
        :param big_gap: отступ между основным столбцом и кнопками возврата назад/в главное меню
        """
        Showable.__init__(self)
        self.color = color
        self.x_center = x_center
        self.y_top = y_top
        self.button_array = []
        self.button_text_array = button_text_array
        self.gap = gap
        self.big_gap = big_gap
        self.main = main
        self.back = back
        self.main_button = Button(self.x_center, 0, 'В главное меню', self.color)
        self.back_button = Button(self.x_center, 0, 'Назад', self.color)
        self.h = def_image.get_height()
        self.init_buttons()
        self.init_back_buttons()

    def init_buttons(self):
        """
        Добавляет кнопки в столбец
        """
        for i in range(len(self.button_text_array)):
            text = self.button_text_array[i]
            self.button_array.append(Button(self.x_center, self.y_top + self.h / 2 + i * (self.h + self.gap),
                                            text, self.color))

    def init_back_buttons(self):
        """
        Добавляет кнопки возврата
        """
        if self.back:
            self.back_button.set_y(self.bottom() + self.big_gap - self.h / 2)
            self.button_array.append(self.back_button)
            if self.main:
                self.main_button.set_y(self.bottom() + self.big_gap + self.h / 2 + self.gap)
                self.button_array.append(self.main_button)
        else:
            if self.main:
                self.main_button.set_y(self.bottom() + self.big_gap - self.h / 2)
                self.button_array.append(self.main_button)

    def blit(self):
        """
        Рисует столбец кнопок
        """
        for button in self.button_array:
            button.blit(self.screen)

    def check(self, event):
        """
        Проверяет нажатие на какую-либо из кнопок столбца
        :param event: событие pygame
        :return: номер нажатой кнопки по вертикали (самая верхняя - 1) или 0, если ни одна не нажата;
        -1 - кнопка возврата назад, -2 - кнопка возврата в главное меню
        """
        num = 0
        for i in range(len(self.button_array)):
            button = self.button_array[i]
            if button.check(event):
                num = i + 1
                break
        if self.main:
            if self.main_button.check(event):
                num = -2
        if self.back:
            if self.back_button.check(event):
                num = -1
        return num

    def bottom(self):
        """
        Возвращает нижнюю координату столбца по вертикали
        """
        if self.back:
            if self.main:
                add = self.big_gap + 2 * self.h
            else:
                add = self.big_gap + self.h - self.gap
        else:
            if self.main:
                add = self.big_gap + self.h - self.gap
            else:
                add = - self.gap
        return self.y_top + len(self.button_array) * (self.gap + self.h) + add


class Menu(Showable):
    def __init__(self, grid: ButtonGrid, link_array: list, text, color, bg_filename, back=0, x=-1, y=-1, gap=30,
                 size=40, font='arial'):
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
        :param size: размер текста меню
        :param font: шрифт текста меню
        """
        Showable.__init__(self)
        self.grid = grid
        self.text = text
        self.x_inp = x
        self.y_inp = y
        self.x = 0
        self.y = 0
        self.color = color
        self.bg = Background(Path('images', bg_filename).resolve())
        self.gap = gap
        self.link_array = link_array
        self.back = back
        self.font = font
        self.size = size
        self.text_surface = self.get_text()
        self.get_coords()
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
        text_surface = font.render(self.text, True, self.color)
        return text_surface

    def put_text(self):
        """
        Помещает текст меню на экран
        """
        self.screen.blit(self.text_surface, (self.x, self.y))

    def blit(self):
        """
        Выводит меню на экран
        """
        self.bg.blit()
        self.grid.blit()
        self.put_text()

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
        """
        self.text = new_text
        self.text_surface = self.get_text()
        self.get_coords()


class GameMenu(Menu):
    def __init__(self, grid: ButtonGrid, link_array: list, text, color, bg_filename, back=0, x=-1, y=-1, gap=30,
                 game=None):
        """
        Конструктор класса игровых меню
        :param game: название игры, происходящей в меню
        """
        Menu.__init__(self, grid, link_array, text, color, bg_filename, back, x, y, gap)
        self.game = game
