"""
Это также реализация игры Блэк Джек на Python,
но она структурирована по-другому.
Вместо использования отдельных модулей для различных частей игры,
все классы и функции размещены в одном файле для более простой организации и реализации.
А также это консольное приложение для максимального упрощения
и смещения фокуса разработки на логику игры
"""

import random


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                      for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(self.card_value(card) for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def card_value(self, card):
        if card.value == 'A':
            return 11
        if card.value.isdigit():
            return int(card.value)
        return 10

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def player_turn(self):
        while True:
            print("\nYour hand:", self.player_hand)
            print("Total value:", self.player_hand.get_value())

            choice = input("Do you want to hit or stand? (h/s): ").strip().lower()
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal_card())
                if self.player_hand.get_value() > 21:
                    return False
            elif choice == 's':
                return True
            else:
                print("Invalid choice! Please enter 'h' or 's'.")
                continue

    def dealer_turn(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
            print("Dealer hits.")

        print("\nDealer's hand:", self.dealer_hand)
        print("Total value:", self.dealer_hand.get_value())
        return self.dealer_hand.get_value() <= 21

    def play_game(self):
        print("Welcome to Blackjack!")
        self.deal_initial_cards()

        if not self.player_turn():
            print("\nBust! You lose.")
            return

        if not self.dealer_turn():
            print("\nDealer busts! You win.")
            return

        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        if player_value > dealer_value:
            print("\nYou win!")
        elif player_value < dealer_value:
            print("\nDealer wins!")
        else:
            print("\nIt's a tie!")


def main():
    game = Blackjack()
    game.play_game()


if __name__ == "__main__":
    main()
