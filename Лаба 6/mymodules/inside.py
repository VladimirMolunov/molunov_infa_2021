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


def inside_rounded_rect(position, x, y, w, h, rx, ry):
    """
    Проверяет попадание курсора в момент клика внутрь скругленного прямоугольника
    :param position: координаты курсора в момент клика (кортеж из 2 элементов - координаты по x и y)
    :param x: левая координата скругленного прямоугольника по горизонтали
    :param y: верхняя координата скругленного прямоугольника по вертикали
    :param w: ширина скругленного прямоугольника
    :param h: высота скругленного прямоугольника
    :param rx: радиус скругления по горизонтали
    :param ry: радиус скругления по вертикали
    :return: True, если точка клика попадает в скругленный прямоугольник, False иначе
    """
    return True if ((x + rx <= position[0] <= x + w - rx) and (y <= position[1] <= y + h))\
                   or ((x <= position[0] <= x + w) and (y + ry <= position[1] <= y + h - ry))\
                   or (inside_ellipse(position, x, y, rx, ry)) \
                   or (inside_ellipse(position, x + w - 2 * rx, y, rx, ry)) \
                   or (inside_ellipse(position, x, y + h - 2 * ry, rx, ry)) \
                   or (inside_ellipse(position, x + w - 2 * rx, y + h - 2 * ry, rx, ry)) else False


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
    xscale = target.r / 190 * ratio
    yscale = target.r / 500
    if target.faces_right:
        a1 = inside_ellipse(position, x + xscale * 210, y, xscale * 140, yscale * 120)
        a2 = inside_ellipse(position, x + 265 * xscale, y + yscale * 83, xscale * 115, yscale * 75)
        a3 = inside_rounded_rect(position, x + xscale * 0, y + yscale * 153, xscale * 330, yscale * 238, xscale * 40,
                                 yscale * 40)
        a4 = inside_ellipse(position, x + xscale * 130, y + yscale * 360, xscale * 60, yscale * 70)
        a5 = inside_ellipse(position, x + xscale * 293, y + yscale * 334, xscale * 57, yscale * 80)
        a6 = inside_rect(position, x + xscale * 70, y + yscale * 300, xscale * 119, yscale * 130)
        a7 = inside_rect(position, x + xscale * 236, y + yscale * 350, xscale * 114, yscale * 64)
        a8 = inside_rect(position, x + xscale * 70, y + yscale * 120, xscale * 280, yscale * 273)
        a9 = inside_rect(position, x + xscale * 85, y + yscale * 363, xscale * 250, yscale * 50)
        return True if a1 or a2 or a3 or a4 or a5 or a6 or a7 or a8 or a9 else False
    else:
        a1 = inside_ellipse(position, x + xscale * 30, y, xscale * 140, yscale * 120)
        a2 = inside_ellipse(position, x, y + yscale * 83, xscale * 115, yscale * 75)
        a3 = inside_rounded_rect(position, x + xscale * 50, y + yscale * 153, xscale * 330, yscale * 238, xscale * 40,
                                 yscale * 40)
        a4 = inside_ellipse(position, x + xscale * 190, y + yscale * 360, xscale * 60, yscale * 70)
        a5 = inside_ellipse(position, x + xscale * 30, y + yscale * 334, xscale * 57, yscale * 80)
        a6 = inside_rect(position, x + xscale * 191, y + yscale * 300, xscale * 119, yscale * 130)
        a7 = inside_rect(position, x + xscale * 30, y + yscale * 350, xscale * 114, yscale * 64)
        a8 = inside_rect(position, x + xscale * 30, y + yscale * 120, xscale * 280, yscale * 273)
        a9 = inside_rect(position, x + xscale * 45, y + yscale * 363, xscale * 250, yscale * 50)
        return True if a1 or a2 or a3 or a4 or a5 or a6 or a7 or a8 or a9 else False
