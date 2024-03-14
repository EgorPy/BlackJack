""" Game logic objects """

import random
from messages import cards_values_messages, cards_suits_messages


class Card:
    """ Represents game card """

    def __init__(self, value: int, suit: int):
        # value can be from 2 to 14
        # suit can be from 0 to 3

        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{cards_values_messages[self.value]} {cards_suits_messages[self.suit]}"


class Deck:
    """ Represents deck (full amount of cards in game) """

    def __init__(self):
        self.cards = [Card(value, suit) for value in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                      for suit in [0, 1, 2, 3]]
        random.shuffle(self.cards)

    def deal_card(self):
        """ Gives player one card from the deck """

        return self.cards.pop()


class Player:
    """ Player logic class """

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """ Adds one card to the player """
        self.cards.append(card)

    def get_value(self):
        """ Calculate the total value of the player """

        value = sum(self.get_card_value(card) for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 14)
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    @staticmethod
    def get_card_value(card):
        """ Calculate value of one card of the player """

        if card.value == 14:
            return 11
        if card.value < 11:
            return card.value
        return 10

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)
