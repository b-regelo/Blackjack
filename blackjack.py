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
            player_name = input(f"Player {n + 1}, what's your name?\n")
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
            player_bet = player.make_bet(player_answer)

            if player_bet == 0:
                self.players.remove(player)
                print(f'{player.name} left the table with {player.balance}$')
            else:
                bets[player.name] = player_bet
                print(f'{player.name} bets {player_bet}$')

        return bets
    
    def _ask_player_choice(self, player, bet):
        self._present_results(player, bet)
        if self._is_bust(player.cards):
            return
        
        choice = input(f'{player.name} hit or stand?\n')
        if choice.lower() == 'hit':
            card = self.card_shoe.get_card()
            player.receive_card(card)
            time.sleep(1)
            print(f'{player.name} gets {card}')
        elif choice.lower() == 'stand':
            return
        
        self._ask_player_choice(player, bet)

    def _calculate_points(self, cards):
        aces = [card for card in cards if card[0] == 'A']
        points = 0
        for card in cards:
            points += self.card_shoe.check_card_value(card)

        while len(aces) > 0 and points > 21:
            aces.pop(0)
            points -= 10
        
        return points
    
    def _present_results(self, player, bet):
        player_name = player.name
        player_cards = ''

        while len(player_name) < 8:
            player_name += ' '
        
        for card in player.cards:
            player_cards += card + '|'
        
        result_string = f'{player_name}| Bet: {bet}$ | Points: {self._calculate_points(player.cards)} | Cards: {player_cards}'
        result_string += " BLACKJACK!!!" if self._has_blackjack(player.cards) else ''
        result_string += " BUST!" if self._is_bust(player.cards) else ''
        print(result_string)

    def _has_blackjack(self, cards):
        if len(cards) == 2 and self._calculate_points(cards) == 21:
            return True
        else:
            return False
        
    def _is_bust(self, cards):
        if self._calculate_points(cards) > 21:
            return True
        else:
            return False
    
    def _deal_dealer_cards(self, curr_dealer_cards):
        new_dealer_cards = curr_dealer_cards

        if len(new_dealer_cards) == 0:
            dealer_card = self.card_shoe.get_card()
            new_dealer_cards.append(dealer_card)
            time.sleep(1)
            print(f'Dealer gets {dealer_card}')
            return new_dealer_cards

        while self._calculate_points(new_dealer_cards) < 17:
            new_card = self.card_shoe.get_card()
            new_dealer_cards.append(new_card)
            time.sleep(1)
            print(f'Dealer gets {new_card}')

        if self._has_blackjack(new_dealer_cards):
                print('Dealer: BLACKJACK!!!')

        cards_string = ''
        for card in new_dealer_cards:
            cards_string += card + '|'
        result_string = f'Dealer  | Points: {self._calculate_points(new_dealer_cards)} | Cards: {cards_string}'
        result_string += " BLACKJACK!!!" if self._has_blackjack(new_dealer_cards) else ''
        result_string += " BUST!" if self._is_bust(new_dealer_cards) else ''
        print(result_string)    
        return new_dealer_cards
            

    def _play_round(self):
        # Betting
        bets = self._ask_bets()
        if len(self.players) == 0:
            return
        
        # Card Dealing
        dealer_cards = []
        self.card_shoe.shuffle()
        self._deal_player_cards()
        dealer_cards = self._deal_dealer_cards(dealer_cards)
        self._deal_player_cards()
        print('-------------------------')
        for player in self.players:
            self._present_results(player, bets[player.name])
        print('-------------------------')

        # Player Choices
        for player in self.players:
            if self._has_blackjack(player.cards):
                print(f'{player.name}: BLACKJACK!!!')
                break
            self._ask_player_choice(player, bets[player.name])
            print('-------------------------')
        
        dealer_cards = self._deal_dealer_cards(dealer_cards)
        
        for player in self.players:
            player.remove_cards()

    def start_game(self):
        print("Welcome to Bruno Regelo's BLACKJACK CASINO!!!")
        self.create_players()
        print('-------------------------')
        while len(self.players) > 0:
            self._play_round() 
            print('-------------------------')
        print('Come back again!')


        


# Set up game
blackjack_game = Game(1, 6)
blackjack_game.start_game()

        