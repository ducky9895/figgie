import time
import random
import threading
import json

from figgie.env.board import Board, OrderBook
from figgie.agents.ducky import DuckyAgent
from figgie.agents.random import RandomAgent

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def create_agent(agent_type, name):
    if agent_type == "DuckyAgent":
        return DuckyAgent(name)
    elif agent_type == "RandomAgent":
        return RandomAgent(name)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

def agent_action(agent, board, order_book, stop_event):
    while not stop_event.is_set():
        action = agent.decide_action(board, order_book)
        if action:
            suit, action_type, price = action
            print(f"{agent.name} decides to {action_type} {suit} at price {price}")
            if action_type == "bid":
                order_book.place_bid(agent.name, suit, price)
            elif action_type == "ask":
                order_book.place_ask(agent.name, suit, price)

        time.sleep(random.uniform(1, 5))  # Small delay to simulate trading actions

def main(config_file='config.json'):
    config = load_config(config_file)
    num_players = config["num_players"]
    num_rounds = config["num_rounds"]
    trading_period = config["trading_period"]
    player_ids = config["player_ids"]
    agent_config = config["agents"]

    board = Board(num_players, player_ids=player_ids)
    order_book = OrderBook(board)

    agents = {}
    for player_id, agent_type in agent_config.items():
        agents[player_id] = create_agent(agent_type, player_id)

    for r in range(num_rounds):
        print(f"Round {r + 1}")
        board.cards = board.initialize_cards()
        board.hands = board.deal_cards()
        print(board.hands)
        
        stop_event = threading.Event()
        threads = []
        
        for agent in agents.values():
            thread = threading.Thread(target=agent_action, args=(agent, board, order_book, stop_event))
            threads.append(thread)
            thread.start()
        
        time.sleep(trading_period)
        stop_event.set()
        
        for thread in threads:
            thread.join()
        
        winners, max_goal_cards, score = board.settle()
        print(f"Funds after round {r + 1}: {score}")
        print(f"Winners: {winners} with {max_goal_cards} goal suit cards")
    
    print("Game Over")


if __name__ == "__main__":
    main()
