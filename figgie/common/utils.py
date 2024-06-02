suit_pairs = {
    'Diamonds': 'Hearts',
    'Hearts': 'Diamonds',
    'Clubs': 'Spades',
    'Spades': 'Clubs'
}


def print_board_state(game_state):
    for player, hand in game_state.hands.items():
        print(f"Player {player}'s hand: {hand}")
