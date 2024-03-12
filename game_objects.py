""" Game logic objects """

import random
from messages import hearts_message, diamonds_message, clubs_message, spades_message


class Card:
    """ Represents game card """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} {self.suit}"


class Deck:
    """ Represents deck (multiple amount of cards in game) of cards """

    def __init__(self):
        self.cards = [Card(value, suit) for value in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
                      for suit in [hearts_message, diamonds_message, clubs_message, spades_message]]
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
        num_aces = sum(1 for card in self.cards if card.value == "A")
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    @staticmethod
    def get_card_value(card):
        """ Calculate value of one card of the player """

        if card.value == "A":
            return 11
        if card.value.isdigit():
            return int(card.value)
        return 10

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)
