""" Классы, представляющие логику игровых объектов """

import random
from messages import cards_values_messages, cards_suits_messages


class Card:
    """ Представляет карту """

    def __init__(self, value: int, suit: int):
        # value может быть от 2 до 14
        # suit может быть от 0 до 3

        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{cards_values_messages[self.value]} {cards_suits_messages[self.suit]}"


class Deck:
    """ Представляет колоду карт """

    def __init__(self):
        self.cards = [Card(value, suit) for value in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                      for suit in [0, 1, 2, 3]]
        random.shuffle(self.cards)

    def deal_card(self):
        """ Выдаёт игроку одну карту из колоды """

        return self.cards.pop()


class Player:
    """ Представляет логику игрока в Блэк Джек """

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """ Добавляет одну карту """

        self.cards.append(card)

    def get_value(self):
        """ Вычисляет общий счёт игрока """

        value = sum(self.get_card_value(card) for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 14)
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    @staticmethod
    def get_card_value(card):
        """ Вычисляет счёт одной карты игрока """

        if card.value == 14:
            return 11
        if card.value < 11:
            return card.value
        return 10

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)
