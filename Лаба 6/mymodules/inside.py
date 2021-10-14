import pygame
pygame.init()


def inside_rect(position, x, y, w, h):
    """
    Проверяет попадание курсора в момент клика внутрь прямоугольника
    :param position: координаты курсора в момент клика (кортеж из 2 элементов - координаты по x и y)
    :param x: левая координата прямоугольника по горизонтали
    :param y: верхняя координата прямоугольника по вертикали
    :param w: ширина прямоугольника
    :param h: высота прямоугольника
    :return: True, если точка клика попадает в прямоугольник, False иначе
    """
    return True if ((x <= position[0] <= x + w) and (y <= position[1] <= y + h)) else False


def inside_circle(position, x, y, r):
    """
    Проверяет попадание курсора в момент клика внутрь круга
    :param position: координаты курсора в момент клика (кортеж из 2 элементов - координаты по x и y)
    :param x: координата центра круга по горизонтали
    :param y: координата центра круг по вертикали
    :param r: радиус круга
    :return: True, если точка клика попадает в круг, False иначе
    """
    return True if ((position[0] - x) ** 2 + (position[1] - y)**2 <= r ** 2) else False


def inside_rounded_rect(position, x, y, w, h, r):
    """
    Проверяет попадание курсора в момент клика внутрь скругленного прямоугольника
    :param position: координаты курсора в момент клика (кортеж из 2 элементов - координаты по x и y)
    :param x: левая координата скругленного прямоугольника по горизонтали
    :param y: верхняя координата скругленного прямоугольника по вертикали
    :param w: ширина скругленного прямоугольника
    :param h: высота скругленного прямоугольника
    :param r: радиус скругления
    :return: True, если точка клика попадает в скругленный прямоугольник, False иначе
    """
    return True if ((x + r <= position[0] <= x + w - 2 * r) and (y <= position[1] <= y + h))\
                   or ((x <= position[0] <= x + w) and (y + r <= position[1] <= y + h - 2 * r))\
                   or (inside_circle(position, x + r, y + r, r)) \
                   or (inside_circle(position, x + w - r, y + r, r)) \
                   or (inside_circle(position, x + r, y + h - r, r)) \
                   or (inside_circle(position, x + w - r, y + h - r, r)) else False


def inside_ellipse(position, x, y, half_w, half_h):
    """
    Проверяет попадание курсора в момент клика внутрь эллипса
    :param position: координаты курсора в момент клика (кортеж из 2 элементов - координаты по x и y)
    :param x: левая координата прямоугольника, задающего эллипс, по горизонтали
    :param y: верхняя координата прямоугольника, задающего эллипс, по вертикали
    :param half_w: половина ширины эллипса
    :param half_h: половина высоты эллипса
    :return: True, если точка клика попадает в эллипс, False иначе
    """
    return True if (half_h ** 2 * (position[0] - x - half_w) ** 2 + half_w ** 2 * (position[1] - y - half_h) ** 2 <=
                    (half_w * half_h) ** 2) else False


def inside_amogus(position, target, ratio):
    """
    Проверяет попадание курсора в момент клика внутрь данной мишени
    :param position: позиция курсора в момент клика (кортеж из двух координат - по x и y)
    :param target: мишень (объект класса Amogus)
    :param ratio: отношение высоты мишени к половине её ширины
    :return: True, если точка клика попадает в мишень, False иначе
    """
    x = target.x - int(target.r * ratio)
    y = target.y - int(target.r / 2)
    scale = target.r / 500

    a1 = inside_ellipse(position, x + scale * 30, y, scale * 140, scale * 120)
    a2 = inside_ellipse(position, x, y + scale * 83, scale * 115, scale * 75)
    a3 = inside_rounded_rect(position, x + scale * 50, y + scale * 153, scale * 330, scale * 238, scale * 40)
    a4 = inside_ellipse(position, x + scale * 190, y + scale * 360, scale * 60, scale * 70)
    a5 = inside_ellipse(position, x + scale * 30, y + scale * 334, scale * 57, scale * 80)
    a6 = inside_rect(position, x + scale * 191, y + scale * 300, scale * 119, scale * 130)
    a7 = inside_rect(position, x + scale * 30, y + scale * 350, scale * 114, scale * 64)
    a8 = inside_rect(position, x + scale * 30, y + scale * 120, scale * 280, scale * 273)
    a9 = inside_rect(position, x + scale * 45, y + scale * 363, scale * 250, scale * 50)
    return True if a1 or a2 or a3 or a4 or a5 or a6 or a7 or a8 or a9 else False
