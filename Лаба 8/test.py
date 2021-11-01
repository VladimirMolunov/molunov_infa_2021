import pygame

from modules.classes import Drawable
from modules.buttons import def_image, image_pressed, image_pointed

pygame.init()
screen = pygame.display.set_mode((800, 600))


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
            i.set_colorkey((255, 255, 255))
        self.render = self.image
        self.width = self.render.get_width()
        self.height = self.render.get_height()
        self.text = text
        self.text_color = text_color
        self.x = x
        self.y = y
        self.is_pressed = False
        self.is_pointed = False
        self.put_text()

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
                    self.is_pressed = True
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

    def put_text(self, str):
        """
        Помещает текст на изображения кнопки
        """
        font = pygame.font.SysFont('arial.ttf', int(self.height))
        text = font.render(str, True, self.text_color)
        w = text.get_width()
        h = text.get_height()
        self.image.blit(text, (self.width / 2 - w / 2, self.height / 2 - h / 2))
        self.image_pointed.blit(text, (self.width / 2 - w / 2, self.height / 2 - h / 2))
        self.image_pressed.blit(text, (self.width / 2 - w / 2, self.height / 2 - h / 2))
        print(self.text, self.y)

    def set_image(self):
        """
        Задаёт нужное изображение кнопки
        """
        if self.is_pressed:
            self.render = self.image_pressed
        else:
            if self.is_pointed:
                self.render = self.image_pointed
            else:
                self.render = self.image
        self.width = self.render.get_height()
        self.height = self.render.get_width()

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
        surface.blit(self.render, (self.x - self.width / 2, self.y - self.height / 2))

    def set_y(self, value):
        """
        Переопределяет значение координаты центра кнопки по вертикали
        :param value: новое значение координаты
        """
        self.y = value


class ButtonGrid:
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
        Drawable.__init__(self)
        self.color = color
        self.screen = pygame.display.set_mode((800, 600))
        self.x_center = x_center
        self.y_top = y_top
        self.button_array = []
        self.button_text_array = button_text_array
        self.init_buttons()

    def init_buttons(self):
        """
        Добавляет кнопки в столбец
        """
        for i in range(len(self.button_text_array)):
            text = self.button_text_array[i]
            self.button_array.append(Button(self.x_center, self.y_top + 80 / 2 + i * (80 + 10), text, self.color))


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

    def center(self):
        """
        Возвращает координату центра столбца по горизонтали
        """
        return self.x_center


grid = ButtonGrid((255, 255, 0), 400, 200, ['EEEEEEEEEE', 'rrrrr', 'BOBus'])
clock = pygame.time.Clock()
finished = False
while not finished:
    screen.fill((60, 60, 228))
    grid.blit()
    clock.tick(60)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
