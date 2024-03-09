"""
This file contains main game logic in a Game class
This class is invoked in main.py file
Update method of this class is called every 0.02 seconds (60 FPS (Depends on what the value of self.MAX_FPS is))
"""

import pygame
from objects import *
from messages import *


class Game:
    """
    Root Wars game class
    """

    def __init__(self, app):
        """ Game initialisation """

        # app variables
        self.app = app
        self.mode = "menu"
        self.version = "1.0"

        # app lists
        self.menu_objects = []
        self.info_objects = []

        # game settings variables that you can change (DEFAULT SETTINGS)
        self.scroll_scale = 40
        self.background_image = pygame.transform.scale(pygame.image.load("background.jpg"), [self.app.WIDTH, self.app.HEIGHT])

        # settings variables
        self.SETTINGS_OBJECTS_CREATED = False
        self.FPS_ENABLED = False
        self.fps_label = Label(self, foreground=(0, 255, 0), font_size=40, font_name="Courier").percent(95, 2)

        self.create_menu_objects()

    def create_menu_objects(self):
        """ Init main menu objects """

        self.game_title_label = Label(self, text=game_title_message).percent_y(10)
        self.play_button = Button(self, text=button_play_message).percent_y(35)
        self.info_button = Button(self, text=button_info_message).percent_y(55)
        self.exit_button = Button(self, text=button_exit_message).percent_y(75)

        self.menu_objects.append(self.game_title_label)
        self.menu_objects.append(self.play_button)
        self.menu_objects.append(self.info_button)
        self.menu_objects.append(self.exit_button)

    def create_info_objects(self):
        """ Init info objects """

        self.info_text = Text(self, text=info_text_message.format(self.version)).percent_y(-3)

        self.back_button = Button(self, text=button_back_message).percent(8, 75)

        self.info_objects.append(self.info_text)
        self.info_objects.append(self.back_button)

    def new_game(self):
        """ game variables that you need to reset to make a new game """

        pass

    def create_game_objects(self):
        """ Init game objects """

        self.player_balance = 5000

        self.cards = [Card(self, size=[40, 80], pos=[i * 45, -i * i * 10]) for i in range(40)]

    def change_mode(self, mode):
        """
        Changes mode to a new mode if it's matches one of the possible modes,
        clearing all variables of all modes except settings
        """

        def clear():
            """ Clears all variables of all modes except settings """

            self.menu_objects.clear()
            self.info_objects.clear()

        if mode == "menu":
            self.mode = mode
            clear()
            self.create_menu_objects()
        elif mode == "info":
            self.mode = mode
            clear()
            self.create_info_objects()
        elif mode == "game":
            self.mode = mode
            clear()
            self.create_game_objects()

    def scroll_info_text(self, event):
        """ Scrolls self.info_text on mouse wheel event """

        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0 and self.info_text.pos[1] > -percent_y(self, 3):
                self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale)
            elif event.y > 0 > self.info_text.pos[1]:
                self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale)

    def update(self, mouse_buttons, mouse_position, events, keys):
        """ Main game logic """

        if self.mode == "menu":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.menu_objects:
                obj.update()

            if self.play_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("game")
            if self.info_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("info")
            if self.exit_button.clicked(mouse_buttons, mouse_position):
                self.app.RUN = False

        if self.mode == "info":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.info_objects:
                obj.update()

            for event in events:
                self.scroll_info_text(event)

            if keys[pygame.K_ESCAPE]:
                self.change_mode("menu")

            if self.back_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("menu")

        if self.mode == "game":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            if keys[pygame.K_ESCAPE]:
                self.change_mode("menu")

            for card in self.cards:
                card.update()
