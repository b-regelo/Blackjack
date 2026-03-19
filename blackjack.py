import random
import time


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.cards = []

    def __repr__(self):
        return f'{self.name}: {self.balance}$'
    
    def make_bet(self, bet):
        if bet <= 0:
            return 0
        elif bet > self.balance:
            print(f'Your balance is only {self.balance}!')
            bet = self.balance
        
        self.balance -= bet
        return bet

    def receive_winnings(self, value):
        self.balance += value

    def check_balance(self):
        return self.balance
    
    def receive_card(self, card):
        self.cards.append(card)
    
    def remove_cards(self):
        self.cards = []


class CardShoe:
    suits = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
    cards = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, number_decks):
        self.number_decks = number_decks
        self.card_shoe = [card + suit for _ in range(number_decks)
                                      for suit in CardShoe.suits.values()
                                      for card in CardShoe.cards.keys()]
        random.shuffle(self.card_shoe)
            
    def __repr__(self):
        return f'{self.number_of_decks} Decks of 52 Cards'
    
    def check_card_value(self, card):
        return CardShoe.cards[card]
    
    def shuffle(self):
        random.shuffle(self.card_shoe)

    def get_card(self):
        retrieved_card = self.card_shoe.pop(0)
        self.card_shoe.append(retrieved_card)
        return retrieved_card


class Game:
    def __init__(self, number_players, number_decks):
        self.number_players = number_players
        self.card_shoe = CardShoe(number_decks)
        self.players = []

    def create_players(self):
        for n in range(self.number_players):
            player_name = input(f"Player {n}, what's your name?\n")
            player_balance = int(input(f"Hi {player_name}! Whats's your balance?\n"))
            self.players.append(Player(player_name, player_balance))

    def _distribute_player_cards(self):
        for player in self.players:
            player_card = self.card_shoe.get_card()
            player.receive_card(player_card)
            time.sleep(1)
            print(f'{player.name} gets {player_card}')

    def _ask_bets(self):
        for player in self.players:
            player_answer = int(input(f'{player.name} place your bet:\n'))
            print(type(player_answer))
            player_bet = player.make_bet(player_answer)
            if player_bet == 0:
                self.players.remove(player)
                print(f'{player.name} left the table with {player.balance}$')
            else:
                print(f'{player.name} bets {player_bet}$')

    def play_round(self):
        self._ask_bets()
        self._distribute_player_cards()


# Set up game
blackjack_game = Game(1, 6)
blackjack_game.create_players()
blackjack_game.play_round()

        