""" Полезные математические функции """

import math


def percent_y(game, percent=0):
    """ Вычисляет количество пикселей в данном проценте высоты экрана """

    one_percent = game.app.HEIGHT / 100
    return one_percent * percent


def percent_x(game, percent=0):
    """ Вычисляет количество пикселей в данном проценте ширины экрана """

    one_percent = game.app.WIDTH / 100
    return one_percent * percent


def touched(x1: int, width1: int, x2: int, width2: int, y1: int, height1: int, y2: int, height2: int) -> bool:
    """ Проверяет коллизию 2 объектов """

    if ((x1 <= x2 <= (x1 + width1) and y1 <= y2 <= (y1 + height1)) or
            (x1 <= (x2 + width2) and (x1 + width1) >= x2 and y1 <= (y2 + height2) and (y1 + height1) >= y2)):
        return True
    return False


def deg_to_rad(degree: float) -> float:
    """ Конвертирует градусы в радианы """

    return degree * math.pi / 180


def rad_to_deg(radian: float) -> float:
    """ Конвертирует радианы в градусы """

    return radian * 180 / math.pi


def rgb_to_hex(r=0, g=0, b=0) -> str:
    """ Конвертирует RGB цвет в HEX цвет """

    return "#" + str(hex(r))[2:].rjust(2, "0").upper() + str(hex(g))[2:].rjust(2, "0").upper() + str(hex(b))[2:].rjust(
        2, "0").upper()


def distance_to_obj(pos1=None, pos2=None) -> float:
    """ Вычисляет расстояние до объекта по теореме Пифагора """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    distance = pow(x_distance ** 2 + y_distance ** 2, 0.5)
    return distance


def rotate_to_cord(pos1=None, pos2=None) -> float:
    """
    Вычисляет угол, на который должен повернуться объект,
    расположенный в pos1, чтобы повернуться к координате pos2
    """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    try:
        angle = math.atan(x_distance / y_distance)
        angle = rad_to_deg(angle)
        if pos1[1] > pos2[1]:
            return angle + 180
        else:
            return angle
    except ZeroDivisionError:
        return 0


def add_brightness(color: list, value: int) -> list:
    """ Добавляет яркость к цвету """

    r, g, b = color
    r += value
    g += value
    b += value
    if r > 255:
        err = r - 255
        g += err // 2
        b += err // 2
    if g > 255:
        err = g - 255
        r += err // 2
        b += err // 2
    if b > 255:
        err = b - 255
        g += err // 2
        r += err // 2
    r = 255 if r > 255 else r
    g = 255 if g > 255 else g
    b = 255 if b > 255 else b
    return [r, g, b]


def sub_brightness(color: list, value: int) -> list:
    """ Вычитает яркость от цвета """

    r, g, b = color
    r -= value
    g -= value
    b -= value
    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b
    return [r, g, b]


def check_value(c: int):
    """ Ограничивает диапазон числа c от 0 до 255 """

    if c > 255:
        return 255
    if c < 0:
        return 0
    return c
