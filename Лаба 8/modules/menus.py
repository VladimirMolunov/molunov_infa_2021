import pygame


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
        self.render = self.image
        self.width = self.image.get_height()
        self.height = self.image.get_width()
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
