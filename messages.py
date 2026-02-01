""" File with all in-game messages """

info_text_message = """
Hello

This is a simple Black Jack game.

Written in Python
using Pygame library (SDL)
And my own library
for quick and easy development on Pygame
called Origin

Date of creation 08.03.24
"""

hearts_message = "Hearts"
diamonds_message = "Diamonds"
clubs_message = "Clubs"
spades_message = "Spades"

cards_values_messages = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
    14: "A"
}

cards_suits_messages = {
    0: diamonds_message,
    1: clubs_message,
    2: hearts_message,
    3: spades_message
}

game_end_messages = {
    "player_busts": "You have too many cards.",
    "dealer_busts": "The dealer busted his cards",
    "black_jack": "Black Jack!",
    "player_wins": "You scored more points",
    "dealer_wins": "The dealer scored more points",
    "tie": "You have the same number of points."
}

relative_payments_messages = {
    "player_busts": -1,
    "dealer_busts": 1,
    "black_jack": 1.5,
    "player_wins": 1,
    "dealer_wins": -1,
    "tie": 0
}

# label texts
game_title_message = "Black Jack"
rules_title_message = "Rules"
rules_text_message = """
Blackjack is a classic card game,
also known as "Twenty-one."
The goal of the game is to accumulate as many points as possible, up to 21.

Point distribution:
Number cards: 2 to 10 points
Face cards (Jacks, Kings, and Queens): 10 points
Aces: 11 points unless busted, otherwise 1 point

Before the game begins, a bet must be placed.
It can be from 1 to the player's maximum amount
of money.

A player can request a card by clicking the "Take a Card" button during the game.

A player can also double their bet,
but only once. After doubling, they are immediately
dealt with 1 card. After doubling the bet,
the player can no longer request cards.

After clicking the "Enough" button,
the dealer takes the required number of cards
and reveals their face-down card. After this, the dealer's and player's points are calculated and they are determined as either a Win, Loss, or Tie.

If the player or dealer reaches a score greater than 21, they lose due to busting.

If the player reaches 21 points with two cards (Ace and 10, Jack, Queen, King), they win with Blackjack!

Have fun!
"""
make_bid_message = "Place your bet"
# {} = player balance
your_balance_message = "Your balance: {}"
your_bid_message = "Your bet: "
start_game_message = "Start game"
not_enough_money_message = "Not enough money to bet"
cant_bid_zero_message = "The bet must be greater than 0"
button_hit_message = "Hit"
button_stand_message = "Stay"
# {} = score
score_message = "Your score: {}"
# {} = bid
bid_message = "Bet: {}"
double_bid_message = "Double down"
bid_doubled_message = "The stakes have been doubled"
win_message = "You win!"
lose_message = "You lost"
tie_message = "Draw"
# {} = money
prize_message = "Total: {}"

# button texts
button_play_message = "Play"
button_rules_message = "Rules"
button_info_message = "Info"
button_exit_message = "Exit"
button_back_message = "Back"
