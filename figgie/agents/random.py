from figgie.agents.base import BaseAgent
import random

class RandomAgent(BaseAgent):
    def decide_action(self, board, order_book):
        suit = random.choice(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
        if random.choice([True, False]):
            price = random.randint(1, 50)
            order_book.place_bid(self.name, suit, price)
        else:
            price = random.randint(1, 50)
            order_book.place_ask(self.name, suit, price)

