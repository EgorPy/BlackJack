"""
Библиотека Origin.
Классы для графического представления игровых объектов.
"""

__author__ = "Egor Mironov"

import pygame.draw
from functions import *


class Pos:
    """ Базовый класс для сохранения позиции объектов """

    def __init__(self, pos=None):
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos

    @staticmethod
    def add_pos(pos1: list, pos2: list) -> list:
        """ Складывает координаты """

        return [pos1[0] + pos2[0], pos1[1] + pos2[1]]

    @staticmethod
    def sub_pos(pos1: list, pos2: list) -> list:
        """ Вычитает координаты """

        return [pos1[0] - pos2[0], pos1[1] - pos2[1]]

    @staticmethod
    def inv_sub_pos(pos1: list, pos2: list) -> list:
        """ Вычитает и инвертирует координаты """

        return [pos2[0] - pos1[0], pos2[1] - pos1[1]]

    @staticmethod
    def mul_pos(pos1: list, pos2: list) -> list:
        """ Умножает координаты """

        return [pos1[0] * pos2[0], pos1[1] * pos2[1]]

    @staticmethod
    def div_pos(pos1: list, pos2: list) -> list:
        """ Делит координаты """

        return [pos1[0] / pos2[0], pos1[1] / pos2[1]]

    @staticmethod
    def inv_div_pos(pos1: list, pos2: list) -> list:
        """ Делит и инвертирует координаты """

        return [pos2[0] / pos1[0], pos2[1] / pos1[1]]


class Vector(Pos):
    """ Класс, представляющий вектора """

    def __init__(self, pos1=None, pos2=None):
        super().__init__()
        if pos1 is None:
            self.pos1 = [0, 0]
        else:
            self.pos1 = pos1
        if pos2 is None:
            self.pos2 = [0, 0]
        else:
            self.pos2 = pos2
        self.length = self.get_length()
        self.angle = self.get_angle()

    def get_length(self):
        """ Возвращает длину вектора """

        return distance_to_obj(self.pos1, self.pos2)

    def get_angle(self):
        """ Возвращает угол вектора """

        y = self.sub_pos(self.pos2, self.pos1)[1]
        length = self.get_length()
        return rad_to_deg(math.sin(y / length))


class Surface(Pos):
    """
    Поверхность, которая позволяет графически отображать изображения,
    менять их прозрачность, colorkey и отображать их на экране
    """

    def __init__(self, game, pos=None, size=None, alpha=255, colorkey=None):
        self.game = game

        super().__init__(pos)
        if size is None:
            self.size = [200, 100]
        else:
            self.size = size
        self.alpha = alpha
        self.colorkey = colorkey

        self.create_surface()

    def create_surface(self):
        """ Создаёт поверхность """

        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        self.surface.set_colorkey(self.colorkey)

    def update(self):
        """ Отображает поверхность """

        self.game.app.DISPLAY.blit(self.surface, self.pos)


class Label(Pos):
    """ Надпись. Однострочный текст """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=100, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        self.game = game

        super().__init__(pos)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.smooth = smooth
        self.foreground = foreground
        self.background = background

        self.font = pygame.font.SysFont(font_name, font_size, bold, italic)
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def update(self):
        """ Отображает поверхность надписи на экране """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def update_text(self, text, smooth=None, foreground=None, background=None):
        """ Обновляет значения text, smooth, foreground и background надписи и пересоздаёт её поверхность """

        self.text = str(text)
        if smooth:
            self.smooth = smooth
        if foreground:
            self.foreground = foreground
        if background:
            self.background = background
        self.surface = self.font.render(self.text, self.smooth, self.foreground, self.background)
        self.size = list(self.surface.get_size())

    def center_x(self, y=0):
        """ Центрирует элемент по горизонтали """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, y]
        return self

    def center_y(self, x=0):
        """ Центрирует элемент по вертикали """

        self.pos = [x, (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def center(self):
        """ Размещает элемент в центре экрана """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2,
                    (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def percent_x(self, percent=0, y=None):
        """ Размещает элемент на данном проценте от ширины экрана """

        one_percent = self.game.app.WIDTH / 100
        if y is None:
            self.pos = [percent * one_percent, (self.game.app.HEIGHT - self.size[1]) / 2]
        else:
            self.pos = [percent * one_percent, y]
        return self

    def percent_y(self, percent=0, x=None):
        """ Размещает элемент на данном проценте от высоты экрана """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, percent * one_percent]
        else:
            self.pos = [x, percent * one_percent]
        return self

    def percent(self, percent_x=0, percent_y=0):
        """ Размещает элемент на данном проценте от ширины и высоты экрана """

        one_percent_x = self.game.app.WIDTH / 100
        one_percent_y = self.game.app.HEIGHT / 100
        self.pos = [percent_x * one_percent_x, percent_y * one_percent_y]
        return self


class Button(Label):
    """ Кнопка """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        self.counter = 0
        self.counter_max = 50

    def clicked(self, mouse_buttons, mouse_position):
        """ Проверяет, нажата ли кнопка """

        x1 = mouse_position[0]
        x2 = self.pos[0]
        w2 = self.size[0]
        y1 = mouse_position[1]
        y2 = self.pos[1]
        h2 = self.size[1]
        if self.counter > 0:
            self.counter -= 1
        if mouse_buttons[0] and touched(x1, 1, x2, w2, y1, 1, y2, h2) and self.counter <= 0:
            self.counter = self.counter_max
            return True
        return False


class Text(Label):
    """ Графический элемент интерфейса для отображения многострочного текста """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None, line_height=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        if line_height is None:
            self.line_height = font_size
        else:
            self.line_height = line_height

        self.strings = self.text.split("\n")
        self.strings_count = len(self.strings)
        self.strings = self.text.split("\n")
        self.strings_count = len(self.strings)
        self.surface_list = [self.font.render(i, self.smooth, self.foreground, self.background) for i in self.strings]
        self.pos_list = [[self.pos[0], self.pos[1] + i * self.line_height] for i in range(self.strings_count)]
        self.size_list = [self.surface_list[i].get_size() for i in range(self.strings_count)]

        self.size = [max([self.surface_list[i].get_size()[0] for i in range(self.strings_count)]),
                     self.strings_count * self.line_height]

    def percent_y(self, percent=0, x=None):
        """ Размещает элемент на данном проценте от высоты экрана """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos_list = [
                [(self.game.app.WIDTH - self.size_list[i][0]) / 2,
                 percent * one_percent + i * self.line_height] for i in range(self.strings_count)
            ]
        else:
            self.pos_list = [[x, percent * one_percent + i * self.line_height] for i in range(self.strings_count)]
        return self

    def update_y(self, y, x=None):
        """ Обновляет позицию элемента на данный процент от высоты экрана """

        self.pos[1] = y
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, y + i * self.line_height]
                             for i in range(self.strings_count)]
        else:
            self.pos_list = [[x, y + i * self.line_height] for i in range(self.strings_count)]

    def update(self):
        """ Отображает объект """

        [self.game.app.DISPLAY.blit(self.surface_list[i], self.pos_list[i]) for i in range(self.strings_count)]


class Entry(Button):
    """ Элемент графического интерфейса для ввода текста """

    def __init__(self, game, pos=None, font_name="Segoe UI", font_size=100, bold=False, smooth=True,
                 foreground=(200, 200, 200), text="", background=None, length=4, is_selected=False, is_focused=False):
        super().__init__(game, text, pos, font_name, font_size, bold, smooth=smooth, foreground=foreground, background=background)

        self.length = length
        self.is_selected = is_selected
        self.is_focused = is_focused

    def enter_key(self, key="", all_keys=False):
        """ Вводит символ """

        if not self.is_selected:
            return
        if key == "backspace":
            self.text = self.text[:-1]
            if len(self.text) == 0 and not all_keys:
                self.text = "0"
            return self.update_text(self.text)
        if len(self.text) >= self.length:
            return
        if all_keys:
            self.text += key
        elif key.isdigit():
            if self.text == "0":
                self.text = key
            else:
                self.text += key
        return self.update_text(self.text)

    def clicked(self, mouse_buttons, mouse_position):
        """ Проверяет нажат ли элемент """

        x1 = mouse_position[0]
        x2 = self.pos[0]
        w2 = self.size[0]
        y1 = mouse_position[1]
        y2 = self.pos[1]
        h2 = self.size[1]
        if touched(x1, 1, x2, w2, y1, 1, y2, h2):
            self.is_focused = True
        else:
            self.is_focused = False
        if mouse_buttons[0]:
            if not self.is_selected and self.is_focused:
                self.is_selected = True
                return True
            if not self.is_focused:
                self.is_selected = False
        return False

    def update(self):
        """ Отображает объект """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

        if self.is_selected or self.is_focused:
            pygame.draw.rect(self.game.app.DISPLAY, (0, 255, 255), pygame.Rect(self.pos, self.size), 1)
            return
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground, pygame.Rect(self.pos, self.size), 1)


class Card(Surface):
    """ Графическое представление карты """

    def __init__(self, game, image, image_pos=None, pos=None, size=None, colorkey=(0, 0, 0),
                 stop_show_percent=70, stop_show_coef=25):
        self.game = game
        self.image = image
        if image_pos is None:
            self.image_pos = [0, 0]
        else:
            self.image_pos = image_pos

        super().__init__(game, size=size, pos=pos, colorkey=colorkey)
        self.surface.blit(self.image, self.image_pos)

        # анимации появления
        self.stop_show_percent = stop_show_percent
        self.stop_show_coef = stop_show_coef

    def update(self):
        """ Отображает объект """

        if self.pos[1] < percent_y(self.game, self.stop_show_percent):
            self.pos[1] += (percent_y(self.game, self.stop_show_percent + 1) - self.pos[1]) // self.stop_show_coef
        else:
            self.pos[1] = percent_y(self.game, self.stop_show_percent)

        self.game.app.DISPLAY.blit(pygame.transform.scale(self.surface, self.size), self.pos)
