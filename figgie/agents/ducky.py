from figgie.agents.base import BaseAgent
from figgie.common.utils import suit_pairs
import random
class DuckyAgent(BaseAgent):
    def decide_action(self, board, order_book):
        hand = board.hands[self.name]
        funds = board.funds[self.name]
        bids = order_book.Bid
        asks = order_book.Ask
        
        action_type = random.choice(["bid", "ask", "wait"])
        max_suit = max(hand, key=hand.get)
        target_suit = suit_pairs[max_suit]

        if action_type == "ask":
            if bids[max_suit] and bids[max_suit]['price'] > 20:
                ask_price = bids[max_suit]['price'] + 5
            else:
                ask_price = 20
            return max_suit, "ask", ask_price
        
        elif action_type == "bid" and funds > 0:
            if asks[target_suit] and asks[target_suit]['price'] < 50:
                bid_price = asks[target_suit]['price'] - 5
            else:
                bid_price = 5
            return target_suit, "bid", bid_price
        
        else:
            return None

