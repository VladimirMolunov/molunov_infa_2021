import pygame

from modules.classes import Drawable


class Button:
    def __init__(self, x, y, text, text_color):
        """
        Конструктор класса кнопок
        :param x: координата центра кнопки по горизонтали
        :param y: координата центра кнопки по вертикали
        :param text: текст на кнопке
        """
        self.image = pygame.Surface((0, 0))
        self.image_pointed = pygame.Surface((0, 0))
        self.image_pressed = pygame.Surface((0, 0))
        for i in (self.image, self.image_pressed, self.image_pointed):
            i.set_colorkey((255, 255, 255))
        self.render = self.image
        self.width = self.render.get_height()
        self.height = self.render.get_width()
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
        """
        if self.is_pointed:
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (-1 * self.width / 2 < event.pos[0] - self.x < self.width / 2) and\
                        (-1 * self.height / 2 < event.pos[1] - self.y < self.height / 2):
                    self.is_pressed = True
        else:
            self.is_pressed = False

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
        font = pygame.font.Font('Arial.ttf', int(0.6 * self.height))
        text = font.render(self.text, True, self.text_color)
        w = text.get_width()
        h = text.get_height()
        self.image.blit(text, (self.x - w / 2, self.y - h / 2))
        self.image_pointed.blit(text, (self.x - w / 2, self.y - h / 2))
        self.image_pressed.blit(text, (self.x - w / 2, self.y - h / 2))

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
        self.check_press(event)
        return True if self.check_press(event) else False

    def blit(self, surface: pygame.Surface):
        """
        Рисует кнопку
        :param surface: поверхность рисования
        """
        surface.blit(self.render, (self.x - self.width / 2, self.y - self.height / 2))


class ButtonGrid(Drawable):
    def __init__(self, surface, color, x_center, y_top, button_text_array: list, gap=10):
        """
        Вертикальный столбец из кнопок
        :param surface: поверхность рисования столбца кнопок
        :param color: цвет кнопок в столбце
        :param x_center: координата центра столбца по горизонтали
        :param y_top: координата верхнего края столбца по вертикали
        :param button_text_array: список текстов на кнопках
        :param gap: отступ между кнопками
        """
        Drawable.__init(self)
        self.surface = surface
        self.color = color
        self.x_center = x_center
        self.y_top = y_top
        self.button_array = []
        self.button_text_array = button_text_array
        self.gap = gap

    def init_buttons(self):
        for i in range(len(self.button_text_aray)):
            text = self.button_text_array[i]
            image = pygame.Surface((0, 0))
            h = image.get_height()
            self.button_array.append(Button(self.x_center, self.y_top + h / 2 + i * (h + self.gap), text, self.color))

    def draw(self):
        """
        Рисует столбец кнопок
        """
        for button in self.button_array:
            button.blit(self.surface)

    def check(self):
        """
        Проверяет нажатие на какую-либо из кнопок столбца
        :return: номер нажатой кнопки по вертикали (самая верхняя - 1) или 0, если ни одна не нажата
        """
        num = 0
        for i in range(len(self.button_array)):
            button = self.button_array[i]
            if button.check():
                num = i + 1
                break
        return num
