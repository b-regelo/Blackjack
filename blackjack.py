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
        return CardShoe.cards[card[0]]
    
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

    def _deal_player_cards(self):
        for player in self.players:
            player_card = self.card_shoe.get_card()
            player.receive_card(player_card)
            time.sleep(1)
            print(f'{player.name} gets {player_card}')

    def _ask_bets(self):
        bets = {}

        for player in self.players[:]:
            player_answer = int(input(f'{player.name} place your bet:\n'))
            print(type(player_answer))
            player_bet = player.make_bet(player_answer)

            if player_bet == 0:
                self.players.remove(player)
                print(f'{player.name} left the table with {player.balance}$')
            else:
                bets[player.name] = player_bet
                print(f'{player.name} bets {player_bet}$')

        return bets
    
    def _ask_player_choice(self, player):
        choice = input(f'{player.name} hit or stand?')
        if choice.lower() == 'hit':
            player.receive_card(self.card_shoe.get_card())
        elif choice.lower() == 'stand':
            return
        else: 
            self._ask_player_choice(player)

    def _calculate_player_points(self, player):
        points = 0
        for card in player.cards:
            points += self.card_shoe.check_card_value(card)

        if points > 21 and ('A' in [card[0] for card in player.cards]):
            points -= 10
        
        return points

    def _has_blackjack(self, player):
        if len(player.cards) == 2 and self._calculate_player_points(player) == 21:
            return True
        else:
            return False
        
    def _is_bust(self, player):
        if self._calculate_player_points(player) > 21:
            return True
        else:
            return False

    def play_round(self):
        # Betting
        bets = self._ask_bets()
        if len(self.players) == 0:
            return
        
        # Card Dealing
        dealer_cards = []
        self.card_shoe.shuffle()
        self._deal_player_cards()
        dealer_cards.append(self.card_shoe.get_card())
        self._deal_player_cards()

        # Player Choices
        for player in self.players:
            if self._has_blackjack(player):
                print(f'{player.name}: BLACKJACK!!!')
                break
            
            p
            self._ask_player_choice(player)


        


# Set up game
blackjack_game = Game(1, 6)
blackjack_game.create_players()
blackjack_game.play_round()

        