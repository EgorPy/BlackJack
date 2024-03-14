""" File with all in-game messages """

# {} = game version
info_text_message = """
Привет

Это простая игра Блэк Джек, 
которая была создана для полуфинала олимпиады 
Траектория Будущего в направлении Python

Написана на Python
с помощью библиотеки Pygame (SDL)
И собственной библиотеки
для простой и быстрой разработки на Pygame
под названием Origin

Дата создания 08.03.24

Версия игры: {}
"""

hearts_message = "Черви"
diamonds_message = "Бубны"
clubs_message = "Крести"
spades_message = "Пики"

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
    "player_busts": "У вас перебор карт",
    "dealer_busts": "У крупье перебор карт",
    "black_jack": "Блэк Джек!",
    "player_wins": "Вы набрали больше очков",
    "dealer_wins": "Крупье набрал больше очков",
    "tie": "Вы набрали одинаковое количество очков"
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
game_title_message = "Блэк Джек"
make_bid_message = "Сделайте ставку"
# {} = player balance
your_balance_message = "Ваш баланс: {}"
your_bid_message = "Ваша ставка: "
start_game_message = "Начать игру"
not_enough_money_message = "Недостаточно денег для ставки"
cant_bid_zero_message = "Ставка должна быть больше 0"
button_hit_message = "Взять карту"
button_stand_message = "Хватит"
# {} = score
score_message = "Ваш счёт: {}"
# {} = bid
bid_message = "Ставка: {}"
double_bid_message = "Удвоить ставку"
bid_doubled_message = "Ставка удвоена"
win_message = "Вы победили!"
lose_message = "Вы проиграли"
tie_message = "Ничья"

# button texts
button_play_message = "Играть"
button_info_message = "Информация"
button_exit_message = "Выход"
button_back_message = "Назад"
