import pygame
from pathlib import Path

from modules.classes import Showable, Background
from modules.vars import *

pygame.init()


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
                if event.button == 1:
                    if self.is_pressed:
                        checked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (-1 * self.width / 2 < event.pos[0] - self.x < self.width / 2)\
                            and (-1 * self.height / 2 < event.pos[1] - self.y < self.height / 2):
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
            if (-1 * self.width / 2 < event.pos[0] - self.x < self.width / 2)\
                    and (-1 * self.height / 2 < event.pos[1] - self.y < self.height / 2):
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
