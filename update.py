"""
Данный файл содержит главную логику игры в классе Game
Этот класс вызывается в файле main.py
Метод update этого класса вызывается каждые 0.02 секунды (60 FPS (Зависит от self.MAX_FPS))
"""

import os
import pygame
import config
import webbrowser
import game_objects
from objects import *
from messages import *


class Game:
    """ Класс игры Блэк Джек """

    def __init__(self, app):
        """ Инициализация игры """

        # переменные приложения
        self.app = app
        self.mode = "menu"
        self.version = "1.0"

        # списки с объектами приложения
        self.menu_objects = []
        self.rules_objects = []
        self.info_objects = []
        self.bid_objects = []
        self.game_objects = []
        self.finish_objects = []

        # настройки игры, которые можно менять (стандартные настройки)
        self.scroll_scale = 40
        self.background_image = pygame.transform.scale(pygame.image.load("background.jpg"), [self.app.WIDTH, self.app.HEIGHT])

        self.prev_mouse_pos = [0, 0]

        self.create_menu_objects()

    @staticmethod
    def save_money(money: int):
        """ Сохраняет деньги игрока в файл """

        with open(config.SAVE_MONEY_PATH, "w") as file:
            file.write(str(money))

    def load_money(self, default=5000):
        """ Загружает деньги игрока из файла. Если его не существует, функция вернёт default """

        if os.path.exists(config.SAVE_MONEY_PATH):
            with open(config.SAVE_MONEY_PATH, "r") as file:
                try:
                    return int(file.readline())
                except ValueError:
                    return default
        self.save_money(default)
        return default

    def create_menu_objects(self):
        """ Инициализация объектов меню """

        self.game_title_label = Label(self, text=game_title_message).percent_y(10)
        self.play_button = Button(self, text=button_play_message).percent_y(30)
        self.rules_button = Button(self, text=button_rules_message).percent_y(45)
        self.info_button = Button(self, text=button_info_message).percent_y(60)
        self.exit_button = Button(self, text=button_exit_message).percent_y(75)

        self.menu_objects.append(self.game_title_label)
        self.menu_objects.append(self.play_button)
        self.menu_objects.append(self.rules_button)
        self.menu_objects.append(self.info_button)
        self.menu_objects.append(self.exit_button)

    def create_rules_objects(self):
        """ Инициализация объектов правил """

        self.rules_label = Label(self, text=rules_title_message).center_x()
        self.rules_text = Text(self, text=rules_text_message, font_size=50).center_x()
        self.rules_text.update_y(self.rules_label.size[1] // 2, percent_x(self, 25))
        self.rules_label.pos[1] = self.rules_text.pos_list[0][1] - self.rules_label.size[1] // 2
        self.back_button = Button(self, text=button_back_message).percent(8, 50)

        self.rules_objects.append(self.rules_label)
        self.rules_objects.append(self.rules_text)
        self.rules_objects.append(self.back_button)

    def create_info_objects(self):
        """ Инициализация объектов информации """

        self.info_text = Text(self, text=info_text_message, font_size=50).percent_y(-3, percent_x(self, 25))
        self.bot_button = Button(self, text="True Midjourney", font_size=50, foreground=(0, 200, 255), italic=True).percent(3, 70)
        self.back_button = Button(self, text=button_back_message).percent(8, 50)

        self.info_objects.append(self.info_text)
        self.info_objects.append(self.bot_button)
        self.info_objects.append(self.back_button)

    def create_game_objects(self):
        """ Инициализация объектов игры """

        self.is_bid = True
        self.is_bid_doubled = False
        self.is_finish = False
        self.start_finish_game_counter = False
        self.WIN = False
        self.LOSE = False
        self.TIE = False
        self.finish_game_counter = 0
        self.game_end_state = ""

        self.player_balance = self.load_money(5000)
        self.player_cards_count = 2
        self.dealer_cards_count = 2
        self.bid = 0

        self.CARD_SHOW_STEP = 500

        self.CARD_WIDTH = 160
        self.CARD_HEIGHT = 230
        self.CARD_MARGIN_X = 11.5
        self.CARD_MARGIN_Y = 9

        # переменные для сохранения состояния скролла карт
        self.dragging = False
        self.drag_offset_x = 0
        self.player_cards_width = self.player_cards_count * (self.CARD_WIDTH + self.CARD_MARGIN_X)
        self.dealer_cards_width = self.dealer_cards_count * (self.CARD_WIDTH + self.CARD_MARGIN_X)

        # инициализация игровых объектов логики игры
        self.deck = game_objects.Deck()
        self.player = game_objects.Player()
        self.dealer = game_objects.Player()

        for i in range(self.player_cards_count):
            self.player.add_card(self.deck.deal_card())
        for i in range(self.dealer_cards_count):
            self.dealer.add_card(self.deck.deal_card())

        # колода карт игрока представленная числами от 2 до 14
        x1 = [card.value for card in self.player.cards]
        y1 = [card.suit for card in self.player.cards]

        # колода карт крупье представленная числами от 2 до 14
        x2 = [card.value for card in self.dealer.cards]
        y2 = [card.suit for card in self.dealer.cards]
        x2[0] = 15
        y2[0] = 2

        self.player_cards = [Card(
            self, pygame.transform.scale(pygame.image.load("cards.png"), (2529, 947)),
            image_pos=[-(x1[i] - 2) * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                       -y1[i] * (self.CARD_HEIGHT + self.CARD_MARGIN_Y)],
            size=[self.CARD_WIDTH, self.CARD_HEIGHT],
            pos=[(self.app.WIDTH - self.player_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                 -i * self.CARD_SHOW_STEP - self.CARD_HEIGHT]
        ) for i in range(self.player_cards_count)]

        self.dealer_cards = [Card(
            self, pygame.transform.scale(pygame.image.load("cards.png"), (2529, 947)),
            image_pos=[-(x2[i] - 2) * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                       -y2[i] * (self.CARD_HEIGHT + self.CARD_MARGIN_Y)],
            size=[self.CARD_WIDTH, self.CARD_HEIGHT],
            pos=[(self.app.WIDTH - self.dealer_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                 -i * self.CARD_SHOW_STEP - self.CARD_HEIGHT],
            stop_show_percent=10
        ) for i in range(self.dealer_cards_count)]

        self.create_bid_objects()
        self.create_game_widgets()

    def create_game_widgets(self):
        """ Инициализация элементов интерфейса игры """

        self.score_label = Label(self, text=score_message.format(self.player.get_value()), font_size=60).percent(10, 65)
        self.hit_button = Button(self, text=button_hit_message, foreground=(255, 255, 255)).percent(10, 75)
        self.stand_button = Button(self, text=button_stand_message, foreground=(255, 255, 255)).percent(10, 85)

        self.bid_label = Label(self, text=bid_message.format(self.bid), font_size=60).percent(75, 65)
        self.double_bid_button = Button(self, text=double_bid_message, foreground=(255, 255, 255)).percent(75, 75)

        self.borders = Surface(self, pos=[0, self.app.HEIGHT - percent_y(self, 35)], size=[self.app.WIDTH, percent_y(self, 35)],
                               colorkey=(0, 0, 0), alpha=50)
        self.borders.surface.fill((200, 200, 200))
        pygame.draw.rect(self.borders.surface, (0, 0, 0), pygame.Rect([percent_x(self, 30), 0],
                                                                      [percent_x(self, 40), self.borders.size[1]]),
                         border_radius=30)

        self.game_objects.append(self.hit_button)
        self.game_objects.append(self.stand_button)
        self.game_objects.append(self.score_label)
        self.game_objects.append(self.bid_label)
        self.game_objects.append(self.double_bid_button)

    def create_bid_objects(self):
        """ Инициализация объектов фазы ставки в игре """

        self.bid_main_label = Label(self, text=make_bid_message).percent_y(10)
        self.balance_label = Label(self, text=your_balance_message.format(self.player_balance), font_size=70).percent_y(35)
        self.cant_play_label = Label(self, font_size=100, foreground=(255, 0, 0))
        self.your_bid_label = Label(self, text=your_bid_message, font_size=70).percent_y(55)
        self.bid_entry = Entry(self, text=str(self.player_balance), length=len(str(self.player_balance)), font_size=70)
        self.your_bid_label.pos[0] -= self.bid_entry.size[0] // 2
        self.bid_entry.pos = [self.your_bid_label.pos[0] + self.your_bid_label.size[0], self.your_bid_label.pos[1]]
        self.start_game_button = Button(self, text=start_game_message).percent_y(75)
        self.back_button = Button(self, text=button_back_message).percent(8, 80)

        self.bid_objects.append(self.bid_main_label)
        self.bid_objects.append(self.balance_label)
        self.bid_objects.append(self.cant_play_label)
        self.bid_objects.append(self.your_bid_label)
        self.bid_objects.append(self.bid_entry)
        self.bid_objects.append(self.start_game_button)
        self.bid_objects.append(self.back_button)

    def change_mode(self, mode):
        """
        Меняет фазу приложения на другую
        И очищает все списки с объектами приложения
        """

        def clear():
            """ Очищает все списки с объектами приложения """

            self.menu_objects.clear()
            self.bid_objects.clear()
            self.game_objects.clear()
            self.rules_objects.clear()
            self.info_objects.clear()
            self.finish_objects.clear()

        self.mode = mode
        clear()
        if mode == "menu":
            self.create_menu_objects()
        elif mode == "rules":
            self.create_rules_objects()
        elif mode == "info":
            self.create_info_objects()
        elif mode == "game":
            self.create_game_objects()

    def scroll_info_text(self, event):
        """ Позволяет скролить self.info_text """

        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0 and self.info_text.pos[1] > -percent_y(self, 3):
                self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale, x=percent_x(self, 25))
            elif event.y > 0 > self.info_text.pos[1]:
                self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale, x=percent_x(self, 25))

    def scroll_rules_text(self, event):
        """ Позволяет скролить текст и надпись с правилами """

        if event.type == pygame.MOUSEWHEEL:
            self.rules_label.pos[1] += event.y * self.scroll_scale
            if self.rules_label.pos[1] < -self.rules_label.size[1] // 2 + self.app.HEIGHT - self.rules_text.size[1]:
                self.rules_label.pos[1] = -self.rules_label.size[1] // 2 + self.app.HEIGHT - self.rules_text.size[1]
            if self.rules_label.pos[1] > self.app.HEIGHT - self.rules_label.size[1] // 2 - self.rules_text.size[1] // 2:
                self.rules_label.pos[1] = self.app.HEIGHT - self.rules_label.size[1] // 2 - self.rules_text.size[1] // 2

            self.rules_text.update_y(self.rules_text.pos[1] + event.y * self.scroll_scale, percent_x(self, 25))
            if self.rules_text.pos_list[0][1] < self.app.HEIGHT - self.rules_text.size[1]:
                self.rules_text.update_y(self.app.HEIGHT - self.rules_text.size[1], percent_x(self, 25))
            if self.rules_text.pos_list[0][1] > self.app.HEIGHT - self.rules_text.size[1] // 2:
                self.rules_text.update_y(self.app.HEIGHT - self.rules_text.size[1] // 2, percent_x(self, 25))

    def check_start_game(self):
        """ Проверяет, может ли игрок зайти в игру с его ставкой """

        bid = int(self.bid_entry.text)
        if bid > self.player_balance:
            self.cant_play_label.update_text(not_enough_money_message)
            self.cant_play_label.percent_y(42)
            return
        if bid <= 0:
            self.cant_play_label.update_text(cant_bid_zero_message)
            self.cant_play_label.percent_y(42)
            return
        self.bid = bid
        self.bid_label.update_text(bid_message.format(self.bid))
        self.is_bid = False

    def add_player_card(self):
        """ Выдаёт игроку одну карту из колоды """

        self.player.add_card(self.deck.deal_card())
        self.score_label.update_text(score_message.format(self.player.get_value()))
        x1 = [card.value for card in self.player.cards]
        y1 = [card.suit for card in self.player.cards]
        i = self.player_cards_count
        self.player_cards_count += 1
        self.player_cards.append(Card(
            self, pygame.transform.scale(pygame.image.load("cards.png"), (2529, 947)),
            image_pos=[-(x1[i] - 2) * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                       -y1[i] * (self.CARD_HEIGHT + self.CARD_MARGIN_Y)],
            size=[self.CARD_WIDTH, self.CARD_HEIGHT],
            pos=[(self.app.WIDTH - self.player_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                 -i * self.CARD_SHOW_STEP - self.CARD_HEIGHT]
        ))
        self.player_cards_width = self.player_cards_count * (self.CARD_WIDTH + self.CARD_MARGIN_X)
        for i, card in enumerate(self.player_cards):
            card.pos[0] = (self.app.WIDTH - self.player_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X)

        if self.player.get_value() > 21:
            self.LOSE = True
            self.game_end_state = "player_busts"
            self.finish()

    def add_dealer_card(self):
        """ Выдаёт крупье одну карту из колоды """

        self.dealer.add_card(self.deck.deal_card())
        x2 = [card.value for card in self.dealer.cards]
        y2 = [card.suit for card in self.dealer.cards]
        i = self.dealer_cards_count
        self.dealer_cards_count += 1
        self.dealer_cards.append(Card(
            self, pygame.transform.scale(pygame.image.load("cards.png"), (2529, 947)),
            image_pos=[-(x2[i] - 2) * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                       -y2[i] * (self.CARD_HEIGHT + self.CARD_MARGIN_Y)],
            size=[self.CARD_WIDTH, self.CARD_HEIGHT],
            pos=[(self.app.WIDTH - self.dealer_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                 -i * self.CARD_SHOW_STEP - self.CARD_HEIGHT],
            stop_show_percent=10
        ))
        self.dealer_cards_width = self.dealer_cards_count * (self.CARD_WIDTH + self.CARD_MARGIN_X)
        for i, card in enumerate(self.dealer_cards):
            card.pos[0] = (self.app.WIDTH - self.dealer_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X)

    def dealer_turn(self):
        """ Логика крупье """

        while self.dealer.get_value() < 17:
            self.add_dealer_card()
        self.finish_game_counter = 100
        self.start_finish_game_counter = True

        if self.dealer.get_value() > 21:
            self.WIN = True
            self.game_end_state = "dealer_busts"
            self.finish()

    def reveal_dealer_card(self):
        """ Открывает скрытую карту крупье """

        x2 = [card.value for card in self.dealer.cards]
        y2 = [card.suit for card in self.dealer.cards]
        self.dealer_cards = [Card(
            self, pygame.transform.scale(pygame.image.load("cards.png"), (2529, 947)),
            image_pos=[-(x2[i] - 2) * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                       -y2[i] * (self.CARD_HEIGHT + self.CARD_MARGIN_Y)],
            size=[self.CARD_WIDTH, self.CARD_HEIGHT],
            pos=[(self.app.WIDTH - self.dealer_cards_width) // 2 + i * (self.CARD_WIDTH + self.CARD_MARGIN_X),
                 percent_y(self, 7)],
            stop_show_percent=10
        ) for i in range(self.dealer_cards_count)]

    def double_bid(self):
        """ Удваивает ставку игрока """

        if self.player_balance >= self.bid * 2:
            self.is_bid_doubled = True
            self.add_player_card()
            self.bid *= 2
            self.bid_label.update_text(bid_message.format(self.bid))
            self.double_bid_button.update_text(bid_doubled_message)

    def finish(self):
        """ Финиш игры """

        self.reveal_dealer_card()
        self.is_finish = True
        player_value = self.player.get_value()
        dealer_value = self.dealer.get_value()

        if self.game_end_state == "":
            if player_value > dealer_value:
                self.WIN = True
                self.game_end_state = "player_wins"
            elif player_value < dealer_value:
                self.LOSE = True
                self.game_end_state = "dealer_wins"
            else:
                self.TIE = True
                self.game_end_state = "tie"
        if self.player_cards_count == 2 and player_value == 21:
            self.WIN = True
            self.game_end_state = "black_jack"
        self.save_money(self.player_balance + int(self.bid * relative_payments_messages[self.game_end_state]))
        self.create_finish_objects()

    def create_finish_objects(self):
        """ Инициализация объектов финиша игры """

        self.player_state_label = Label(self)
        if self.WIN:
            self.player_state_label.update_text(win_message)
        if self.LOSE:
            self.player_state_label.update_text(lose_message)
        if self.TIE:
            self.player_state_label.update_text(tie_message)
        self.player_state_label.percent_y(35)
        self.description_label = Label(self, text=game_end_messages[self.game_end_state], font_size=70).percent_y(45)
        self.back_button = Button(self, text=button_exit_message, foreground=(255, 255, 255), font_size=70).percent(10, 10)
        self.prize_label = (Label(self, font_size=70,
                                  text=prize_message.format(int(self.bid * relative_payments_messages[self.game_end_state])))
                            .percent_y(55))

        self.finish_objects.append(self.player_state_label)
        self.finish_objects.append(self.description_label)
        self.finish_objects.append(self.prize_label)
        self.finish_objects.append(self.back_button)

    def update(self, mouse_buttons, mouse_position, events, keys):
        """ Основная логика игры """

        if self.mode == "menu":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.menu_objects:
                obj.update()

            if self.play_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("game")
            if self.rules_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("rules")
            if self.info_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("info")
            if self.exit_button.clicked(mouse_buttons, mouse_position):
                self.app.RUN = False

        if self.mode == "rules":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.rules_objects:
                obj.update()

            for event in events:
                self.scroll_rules_text(event)

            if self.back_button.clicked(mouse_buttons, mouse_position) or keys[pygame.K_ESCAPE]:
                self.change_mode("menu")

        if self.mode == "info":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.info_objects:
                obj.update()

            for event in events:
                self.scroll_info_text(event)

            if keys[pygame.K_ESCAPE]:
                self.change_mode("menu")

            if self.bot_button.clicked(mouse_buttons, mouse_position):
                webbrowser.open("https://t.me/TrueMidjourney_bot")
            if self.back_button.clicked(mouse_buttons, mouse_position) or keys[pygame.K_ESCAPE]:
                self.change_mode("menu")

        if self.mode == "game":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            if self.is_bid:
                if self.back_button.clicked(mouse_buttons, mouse_position) or keys[pygame.K_ESCAPE]:
                    self.change_mode("menu")

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.bid_entry.enter_key(pygame.key.name(event.key))

                if self.bid_entry.clicked(mouse_buttons, mouse_position):
                    self.bid_entry.is_selected = True
                if self.start_game_button.clicked(mouse_buttons, mouse_position):
                    self.check_start_game()

                for obj in self.bid_objects:
                    obj.update()

                return

            for card in self.player_cards:
                card.update()
            for card in self.dealer_cards:
                card.update()
            self.borders.update()
            for obj in self.game_objects:
                obj.update()

            if self.is_finish:
                if self.back_button.clicked(mouse_buttons, mouse_position) or keys[pygame.K_ESCAPE]:
                    self.change_mode("menu")

                for obj in self.finish_objects:
                    obj.update()

                return

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in self.player_cards:
                        if touched(card.pos[0], card.size[0], event.pos[0], 1,
                                   card.pos[1], card.size[1], event.pos[1], 1):
                            self.dragging = True
                            self.drag_offset_x = event.pos[0] - card.pos[0]
                            self.prev_mouse_pos = event.pos
                            break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging = False
                if (event.type == pygame.MOUSEMOTION and self.dragging and
                        percent_x(self, 30) < event.pos[0] < percent_x(self, 70)):
                    mouse_dx = event.pos[0] - self.prev_mouse_pos[0]
                    for card in self.player_cards:
                        card.pos[0] += mouse_dx
                    self.prev_mouse_pos = event.pos

            if self.hit_button.clicked(mouse_buttons, mouse_position) and not self.is_finish and not self.is_bid_doubled:
                self.add_player_card()
            if self.stand_button.clicked(mouse_buttons, mouse_position) and not self.is_finish:
                self.dealer_turn()
            if self.double_bid_button.clicked(mouse_buttons, mouse_position) and not self.is_bid_doubled and not self.is_finish:
                self.double_bid()
            if self.start_finish_game_counter:
                if self.finish_game_counter > 0:
                    self.finish_game_counter -= self.app.delta_time * self.app.MAX_FPS
                else:
                    self.finish()
                    self.start_finish_game_counter = False
