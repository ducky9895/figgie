import random
from figgie.common.utils import *

class Board:
    def __init__(self, num_players=4, player_ids=None):
        assert num_players in [4, 5], "Number of players must be 4 or 5"

        self.pot = 200
        self.cards = self.initialize_cards()
        self.initialize_players(num_players, player_ids)
        self.hands = self.deal_cards()
        print(self.hands)

    def initialize_cards(self):
        suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        counts = [12, 10, 10, 8]
        random.shuffle(suits)
        
        twelve_card_suit = suits.pop(0)
        self.goal_suit = suit_pairs[twelve_card_suit]
        
        random.shuffle(suits)   
        suit_counts = {twelve_card_suit: 12}
        for suit, count in zip(suits, counts[1:]):
            suit_counts[suit] = count
        
        cards = [suit for suit, count in suit_counts.items() for _ in range(count)]
        random.shuffle(cards)
        return cards

    def initialize_players(self, num_players, player_ids):
        if player_ids is None:
            player_ids = []
        self.players = player_ids[:]
        
        bot_count = 0
        while len(self.players) < num_players:
            self.players.append(f"bot{bot_count}")
            bot_count += 1

    def deal_cards(self):
        self.hands = {player: {suit: 0 for suit in ['Diamonds', 'Hearts', 'Clubs', 'Spades']} for player in self.players}
        for i, card in enumerate(self.cards):
            player = self.players[i % len(self.players)]
            self.hands[player][card] += 1
        return self.hands

    def settle(self):
        goal_suit_counts = {player: hand[self.goal_suit] for player, hand in self.hands.items()}
        max_goal_cards = max(goal_suit_counts.values())
        winners = [player for player, count in goal_suit_counts.items() if count == max_goal_cards]
        print(f"Winners: {winners} with {max_goal_cards} goal suit cards")

        payouts = {player: 10 * goal_suit_counts[player] for player in self.hands}

        pot_share = self.pot // len(winners)
        for player in self.winners:
            payouts[player] += pot_share
            
        return winners, max_goal_cards, payouts