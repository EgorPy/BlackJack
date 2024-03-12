""" Useful math functions """

import math


def percent_y(game, percent=0):
    """ Calculates screen height in percents """

    one_percent = game.app.HEIGHT / 100
    return one_percent * percent


def percent_x(game, percent=0):
    """ Calculates screen width in percents """

    one_percent = game.app.WIDTH / 100
    return one_percent * percent


def touched(x1: int, width1: int, x2: int, width2: int, y1: int, height1: int, y2: int, height2: int) -> bool:
    """ Checks if one object is touching other object """

    if ((x1 <= x2 <= (x1 + width1) and y1 <= y2 <= (y1 + height1)) or
            (x1 <= (x2 + width2) and (x1 + width1) >= x2 and y1 <= (y2 + height2) and (y1 + height1) >= y2)):
        return True
    return False


def deg_to_rad(degree: float) -> float:
    """ Converts degrees to radians """

    return degree * math.pi / 180


def rad_to_deg(radian: float) -> float:
    """ Converts radians to degrees """

    return radian * 180 / math.pi


def rgb_to_hex(r=0, g=0, b=0) -> str:
    """ Converts rgb value to hex value """

    return "#" + str(hex(r))[2:].rjust(2, "0").upper() + str(hex(g))[2:].rjust(2, "0").upper() + str(hex(b))[2:].rjust(
        2, "0").upper()


def distance_to_obj(pos1=None, pos2=None) -> float:
    """ Gets distance between two positions using Pythagorean theorem """

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
    :param pos1: pos of the object that must be turned
    :param pos2: pos of the object to turn to
    :return: angle to turn to face to given position
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
    """ Adds brightness to given color """

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
    """ Subtracts brightness to given color """

    r, g, b = color
    r -= value
    g -= value
    b -= value
    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b
    return [r, g, b]


def check_value(c: int):
    """ Checks if value is from 0 to 255 """

    if c > 255:
        return 255
    if c < 0:
        return 0
    return c
