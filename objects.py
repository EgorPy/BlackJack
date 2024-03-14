"""
Origin Library.
This file contains all game objects classes.
"""

__author__ = "Egor Mironov"

import pygame.draw
from functions import *


def rotate(image, pos, origin_pos, angle):
    """ Rotate pygame surface to given angle with stable origin position """

    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - origin_pos[0] + min_box[0] - pivot_move[0], pos[1] - origin_pos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    return rotated_image, [origin[0] + 25, origin[1] + 25]


class Pos:
    """ Basic class for interpreting something that has position """

    def __init__(self, pos=None):
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos

    @staticmethod
    def add_pos(pos1: list, pos2: list) -> list:
        """ Adds coordinates """

        return [pos1[0] + pos2[0], pos1[1] + pos2[1]]

    @staticmethod
    def sub_pos(pos1: list, pos2: list) -> list:
        """ Subtracts coordinates """

        return [pos1[0] - pos2[0], pos1[1] - pos2[1]]

    @staticmethod
    def inv_sub_pos(pos1: list, pos2: list) -> list:
        """ Subtracts and inverts coordinates """

        return [pos2[0] - pos1[0], pos2[1] - pos1[1]]

    @staticmethod
    def mul_pos(pos1: list, pos2: list) -> list:
        """ Multiplies coordinates """

        return [pos1[0] * pos2[0], pos1[1] * pos2[1]]

    @staticmethod
    def div_pos(pos1: list, pos2: list) -> list:
        """ Divides coordinates """

        return [pos1[0] / pos2[0], pos1[1] / pos2[1]]

    @staticmethod
    def inv_div_pos(pos1: list, pos2: list) -> list:
        """ Divides and inverts coordinates"""

        return [pos2[0] / pos1[0], pos2[1] / pos1[1]]


class Vector(Pos):
    """ Class that represents vectors """

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
        """ Returns length of a vector """

        return distance_to_obj(self.pos1, self.pos2)

    def get_angle(self):
        """
        Returns vector angle.

        y: vertical size of a vector.
        l: length of a vector.
        """

        y = self.sub_pos(self.pos2, self.pos1)[1]
        length = self.get_length()
        return rad_to_deg(math.sin(y / length))


class Surface(Pos):
    """ Surface class that allows you to set alpha value, colorkey and other cool things to show on pygame window"""

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
        """ Creates pygame surface """

        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        self.surface.set_colorkey(self.colorkey)

    def update(self):
        """ Shows the surface on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)


class Label(Pos):
    """ Label UI object for pygame games. """

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
        """ Shows the surface of label on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def update_text(self, text, smooth=None, foreground=None, background=None):
        """ Updates text, smooth, foreground and background values of label and recreates surface of label """

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
        """ Places label at the center of game app screen width """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, y]
        return self

    def center_y(self, x=0):
        """ Places label at the center of game app screen height """

        self.pos = [x, (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def center(self):
        """ Places label at the center of game app screen width and height """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2,
                    (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def percent_x(self, percent=0, y=None):
        """ Places label at given percent on the game app screen width """

        one_percent = self.game.app.WIDTH / 100
        if y is None:
            self.pos = [percent * one_percent, (self.game.app.HEIGHT - self.size[1]) / 2]
        else:
            self.pos = [percent * one_percent, y]
        return self

    def percent_y(self, percent=0, x=None):
        """ Places label at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, percent * one_percent]
        else:
            self.pos = [x, percent * one_percent]
        return self

    def percent(self, percent_x=0, percent_y=0):
        """ Places label at given percent on the game app screen width and height """

        one_percent_x = self.game.app.WIDTH / 100
        one_percent_y = self.game.app.HEIGHT / 100
        self.pos = [percent_x * one_percent_x, percent_y * one_percent_y]
        return self


class Button(Label):
    """ Button UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        self.counter = 0
        self.counter_max = 50

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if button is clicked or not """

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


class OptionButton(Button):
    """
    OptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    """

    def __init__(self, game, text="", options=None, pos=None, font_name="Segoe UI", font_size=60, bold=False,
                 italic=False, smooth=True, foreground=(200, 200, 200), background=None,
                 current_option=0):
        if options is None:
            self.options = ["Option 1", "Option 2", "Option 3"]
        else:
            self.options = options
        self.current_option = current_option
        self.static_text = text
        self.text = self.static_text + str(self.options[self.current_option])
        super().__init__(game, self.text, pos, font_name, font_size, bold, italic, smooth, foreground, background)
        self.counter_max = 20

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if option button is clicked or not """

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
            self.next_option()

    def next_option(self):
        """ Selects next option to display on option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text + str(self.options[self.current_option])
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def get_current_option(self):
        """ Returns current option value """

        return self.options[self.current_option]


class ColorOptionButton(OptionButton):
    """
    ColorOptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    Option represents RGB color. Option example: (255, 0, 0).
    """

    def __init__(self, game, text="", color_rect_size=None, options=None, pos=None, font_name="Segoe UI", font_size=60,
                 bold=False, italic=False, smooth=True,
                 foreground=(200, 200, 200), background=None, current_option=0, outline=1):
        super().__init__(game, text, options, pos, font_name, font_size, bold, italic, smooth, foreground, background,
                         current_option)
        self.text = self.static_text
        self.outline = outline
        self.update_text(self.text, self.smooth, self.foreground, self.background)
        if options is None:
            self.options = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        else:
            self.options = options
        if color_rect_size is None:
            self.color_rect_size = [self.font_size * 2, self.font_size + 10]
        else:
            self.color_rect_size = color_rect_size

    def update(self):
        """ Shows the surface of label on a game app display and the rectangle with picked color option """

        pygame.draw.rect(self.game.app.DISPLAY, self.options[self.current_option],
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size))
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground,
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size), self.outline)
        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def next_option(self):
        """ Selects next option to display on color option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text
        self.update_text(self.text, self.smooth, self.foreground, self.background)


class Text(Label):
    """
    Text UI object for pygame games.
    This widget allows you to create multiline text.
    """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None, line_height=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        if line_height is None:
            self.line_height = font_size
        else:
            self.line_height = line_height

        self.strings = self.text.split("\n")
        self.strings_count = len(self.strings)
        # self.init_buttons(buttons_foreground)
        self.strings = self.text.split("\n")
        self.strings_count = len(self.strings)
        self.surface_list = [self.font.render(i, self.smooth, self.foreground, self.background) for i in self.strings]
        self.pos_list = [[self.pos[0], self.pos[1] + i * self.line_height] for i in range(self.strings_count)]
        self.size_list = [self.surface_list[i].get_size() for i in range(self.strings_count)]

        self.size = [max([self.surface_list[i].get_size()[0] for i in range(self.strings_count)]),
                     self.strings_count * self.line_height]

    def init_buttons(self, button_color):
        """ If widget's text has <button></button> tag, it will be parsed as button """

        self.buttons_foreground = button_color
        self.button_lines = []
        self.buttons = []
        self.buttons_count = self.text.count("<button>")
        first_index = 0
        last_index = 0
        for i in range(self.buttons_count):
            first_index = self.text.find("<button>", first_index + 1) + 8
            last_index = self.text.find("</button>", last_index + 1)
            self.buttons.append(self.text[first_index:last_index])
        for i in range(self.strings_count):
            if "<button>" in self.strings[i]:
                self.button_lines.append(i)
        self.text = self.text.replace("<button>", "")
        self.text = self.text.replace("</button>", "")
        print(*self.buttons, sep="\n")

    def percent_y(self, percent=0, x=None):
        """ Places Text at given percent on the game app screen height """

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
        """ Updates Text position at given percent on the game app screen height """

        self.pos[1] = y
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, y + i * self.line_height]
                             for i in range(self.strings_count)]
        else:
            self.pos_list = [[x, y + i * self.line_height] for i in range(self.strings_count)]

    def update(self):
        """ Shows the surface of Text on a game app display """

        [self.game.app.DISPLAY.blit(self.surface_list[i], self.pos_list[i]) for i in range(self.strings_count)]


class Entry(Button):
    def __init__(self, game, pos=None, font_name="Segoe UI", font_size=100, bold=False, smooth=True,
                 foreground=(200, 200, 200), text="", background=None, length=4, is_selected=False, is_focused=False):
        super().__init__(game, text, pos, font_name, font_size, bold, smooth=smooth, foreground=foreground, background=background)

        self.length = length
        self.is_selected = is_selected
        self.is_focused = is_focused

    def enter_key(self, key="", all_keys=False):
        """ Enters key to the entry """

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
        """ Checks if button is clicked or not """

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
        """ Display object """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

        if self.is_selected or self.is_focused:
            pygame.draw.rect(self.game.app.DISPLAY, (0, 255, 255), pygame.Rect(self.pos, self.size), 1)
            return
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground, pygame.Rect(self.pos, self.size), 1)


class Line(Vector):
    """ Line class for the Root Wars grid map. """

    def __init__(self, game, pos1=None, pos2=None, color=(255, 255, 255), width=5):
        self.game = game

        super().__init__(pos1, pos2)
        self.color = color
        self.width = width

    def update(self):
        """ Draws the Line on game app display """

        pygame.draw.line(self.game.app.DISPLAY, self.color,
                         [self.pos1[0] + self.game.cords[0], self.pos1[1] + self.game.cords[1]],
                         [self.pos2[0] + self.game.cords[0], self.pos2[1] + self.game.cords[1]],
                         self.width)


class AnimatedRing(Surface):
    """
    Was the first test version of bloom effect.
    Now it's a simple test object that uses smooth animation.
    """

    surface_size = 300

    def __init__(self, game, pos=None, size=100, color=(0, 155, 255), alpha=255, colorkey=None, angle=0, width=4):
        Surface.__init__(self, game, pos, [self.surface_size, self.surface_size], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.size = size
        self.width = width
        self.counter = 0

        self.acceleration = 20
        self.init_size = 10
        self.max_size = self.size

        self.init_max_size = size
        self.init_color = color

        # self.surface.fill((255, 0, 0))
        self.draw_ring()

    def draw_ring(self):
        """ Draws ring on its surface """

        self.surface.fill(self.colorkey)
        pygame.draw.circle(self.surface, sub_brightness(self.color, 100),
                           [self.surface_size // 2, self.surface_size // 2], self.size // 2 + self.width // 2,
                           self.width * 2)
        pygame.draw.circle(self.surface, self.color, [self.surface_size // 2, self.surface_size // 2], self.size // 2,
                           self.width)

    def draw_circle(self):
        """ Draws circle on its surface """

        self.surface.fill(self.colorkey)
        pygame.draw.circle(self.surface, sub_brightness(self.color, 100),
                           [self.surface_size // 2, self.surface_size // 2], self.size // 2 + self.width * 2)
        pygame.draw.circle(self.surface, self.color, [self.surface_size // 2, self.surface_size // 2], self.size // 2)

    def set_alpha(self, alpha: int):
        """ Sets alpha value of the surface """

        self.alpha = alpha
        self.surface.set_alpha(self.alpha)

    def set_size(self, size):
        """ Sets the size value of the surface """

        self.size = size
        self.draw_ring()

    def update(self):
        """ Shows the surface on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

        if self.color[2] < 230:
            self.color = add_brightness(self.color, 8)
        self.draw_ring()

        self.size = (self.counter / (self.counter / 1.1 + 1)) * (self.max_size - self.init_size) + self.init_size
        if self.size > self.max_size:
            self.size = self.max_size
        # self.width = 15 - int(self.size / 10)
        # self.set_alpha(self.size)
        self.set_size(self.size)

        if self.counter < 255:
            self.counter += 1

    def reset(self):
        """ Resets animation properties """

        self.counter = 0
        self.size = self.init_max_size
        self.max_size = self.size
        self.color = self.init_color


class Bloom2(Surface):
    """
    Bloom effects like post-processing.
    Can be implemented in any visual object.
    """

    def __init__(self, game, pos=None, r=50, light_source_r=5, resolution=20, color=(255, 255, 255), alpha=5,
                 colorkey=(0, 0, 0), angle=0):
        Surface.__init__(self, game, pos, [r, r], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.r = r
        self.light_source_r = light_source_r
        self.resolution = resolution
        self.size = [r, r]
        self.intensity = 1
        self.scale = self.r // self.resolution

        self.draw(0)

    def draw(self, r):
        """ Draws bloom light on self surface """

        self.surface.fill(self.colorkey)
        self.surface.set_alpha(self.alpha)
        pygame.draw.circle(self.surface, self.color, [self.r // 2, self.r // 2], self.r // 2 - r)

    def update(self):
        """ Shows the surface on a game app display """

        # rotated_surface, rotated_pos = rotate(self.surface, self.pos, [self.s // 2, self.s // 2], i * self.steps)

        # draw light
        for i in range(self.r // self.scale):
            self.draw(self.r - i * self.scale)
            self.game.app.DISPLAY.blit(self.surface, self.pos)

        # draw light source
        pygame.draw.circle(self.game.app.DISPLAY, add_brightness(self.color, 100),
                           self.add_pos(self.pos, [self.r // 2, self.r // 2]), self.light_source_r)


class Bloom3(Surface):
    """
    Bloom effects like post-processing.
    Can be implemented in any visual object.
    Allows to create glowy lines.
    """

    def __init__(self, game, pos=None, r=50, light_source_r=2, resolution=20, color=(255, 255, 255), alpha=3,
                 colorkey=(0, 0, 0), angle=0):
        Surface.__init__(self, game, pos, [r, r], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.r = r
        self.light_source_r = light_source_r
        self.resolution = resolution
        self.size = [r, r]
        self.intensity = 1
        self.scale = self.r // self.resolution
        self.last_pos = self.pos

        self.draw(0)

    def draw(self, r):
        """ Draws bloom light on self surface """

        self.surface.fill(self.colorkey)
        self.surface.set_alpha(self.alpha)
        pygame.draw.circle(self.surface, self.color, [self.r // 2, self.r // 2], self.r // 2 - r)

    def update(self):
        """ Shows the surface on a game app display """

        # draw light
        for i in range(self.r // self.scale):
            self.draw(self.r - i * self.scale)
            self.game.app.DISPLAY.blit(self.surface, self.sub_pos(self.pos, [self.r // 2, self.r // 2]))

        # draw light source
        pygame.draw.line(self.game.app.DISPLAY, add_brightness(self.color, 100), self.last_pos, self.pos,
                         self.light_source_r * 2)

        self.last_pos = self.pos


class Card(Surface):
    """ Graphic representation of card """

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

        # showing animation variables
        self.stop_show_percent = stop_show_percent
        self.stop_show_coef = stop_show_coef

    def update(self):
        """ Display object """

        if self.pos[1] < percent_y(self.game, self.stop_show_percent):
            self.pos[1] += (percent_y(self.game, self.stop_show_percent + 1) - self.pos[1]) // self.stop_show_coef
        else:
            self.pos[1] = percent_y(self.game, self.stop_show_percent)

        self.game.app.DISPLAY.blit(pygame.transform.scale(self.surface, self.size), self.pos)
