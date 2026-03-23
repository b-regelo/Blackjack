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
        return f'{self.number_decks} Decks of 52 Cards'
    
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
            
            while True:
                try:
                    player_balance = int(input(f"Hi {player_name}! Whats's your balance?\n"))
                    break
                except ValueError:
                    print('Please enter a valid number.')
            
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
            while True:
                try:
                    player_answer = int(input(f'{player.name} place your bet: '))
                    break
                except ValueError:
                    print('Please place a valid bet.')

            player_bet = player.make_bet(player_answer)

            if player_bet == 0:
                self.players.remove(player)
                print(f'{player.name} left the table with {player.balance}$')
            else:
                bets[player.name] = player_bet
                print(f'{player.name} bets {player_bet}$')

        return bets
    
    def _ask_player_choice(self, player, bet):
        self._present_results(player.cards, player.name, bet)

        while True:
            if self._is_bust(player.cards) or self._has_blackjack(player.cards):
                return
            
            choice = input(f'{player.name} hit or stand?\n').lower().strip()
            if choice == 'hit':
                card = self.card_shoe.get_card()
                player.receive_card(card)
                time.sleep(1)
                print(f'{player.name} gets {card}')
                self._present_results(player.cards, player.name, bet)
            elif choice == 'stand':
                return
            else:
                print("Please type 'hit' or 'stand'.")

    def _calculate_points(self, cards):
        aces = [card for card in cards if card[0] == 'A']
        points = 0
        for card in cards:
            points += self.card_shoe.check_card_value(card)

        while len(aces) > 0 and points > 21:
            aces.pop(0)
            points -= 10
        
        return points
    
    def _present_results(self, cards, name='Dealer', bet=0):
        cards_string = ''
        result_string = f'{name:<8}'
        
        for card in cards:
            cards_string += card + '|'
        
        if bet > 0:
            result_string += f'| Bet: {bet}$ '
        
        result_string += f'| Points: {self._calculate_points(cards)} | Cards: {cards_string}'
        result_string += " BLACKJACK!!!" if self._has_blackjack(cards) else ''
        result_string += " BUST!" if self._is_bust(cards) else ''
        print(result_string)

    def _has_blackjack(self, cards):
        return len(cards) == 2 and self._calculate_points(cards) == 21
        
    def _is_bust(self, cards):
        return self._calculate_points(cards) > 21
    
    def _deal_dealer_cards(self, dealer_cards):
        if len(dealer_cards) == 0:
            dealer_card = self.card_shoe.get_card()
            dealer_cards.append(dealer_card)
            time.sleep(1)
            print(f'Dealer gets {dealer_card}')
            return dealer_cards

        while self._calculate_points(dealer_cards) < 17:
            new_card = self.card_shoe.get_card()
            dealer_cards.append(new_card)
            time.sleep(1)
            print(f'Dealer gets {new_card}')

        time.sleep(1)
        if self._has_blackjack(dealer_cards):
            print('Dealer: BLACKJACK!!!')
        elif self._is_bust(dealer_cards):
            print('Dealer: BUST!')

        self._present_results(dealer_cards)   
        return dealer_cards
    
    def _pay_winnings(self, dealer_cards, bets):
        dealer_points = self._calculate_points(dealer_cards)

        for player in self.players:
            if self._is_bust(player.cards) or (self._has_blackjack(dealer_cards) and not self._has_blackjack(player.cards)):
                print(f'{player.name} lost...')
                continue
            
            player_points = self._calculate_points(player.cards)
            player_winnings = 0

            if (self._has_blackjack(player.cards) and self._has_blackjack(dealer_cards)) or (player_points == dealer_points):
                print(f'{player.name} tied.')
                player_winnings = bets[player.name]
            elif self._has_blackjack(player.cards):
                player_winnings = 2.5 * bets[player.name] 
                print(f'{player.name} won {int(player_winnings)}$!!!')
            elif self._is_bust(dealer_cards) or player_points > dealer_points:
                player_winnings = 2 * bets[player.name]
                print(f'{player.name} won {int(player_winnings)}$!!!')
            else:
                print(f'{player.name} lost...')
                continue
            
            player.receive_winnings(player_winnings)

    def _play_round(self):
        # Betting
        bets = self._ask_bets()
        print('-------------------------')
        if len(self.players) == 0:
            return
        
        # Card Dealing
        dealer_cards = []
        self.card_shoe.shuffle()
        self._deal_player_cards()
        dealer_cards = self._deal_dealer_cards(dealer_cards)
        self._deal_player_cards()
        print('-------------------------')
        self._present_results(dealer_cards)
        for player in self.players:
            self._present_results(player.cards, player.name, bets[player.name])
        print('-------------------------')

        # Player Choices
        for player in self.players:
            self._ask_player_choice(player, bets[player.name])
            print('-------------------------')
        
        # Dealer Cards
        dealer_cards = self._deal_dealer_cards(dealer_cards)
        for player in self.players:
            self._present_results(player.cards, player.name, bets[player.name])
        print('-------------------------')
        
        # Payouts
        self._pay_winnings(dealer_cards, bets)
        for player in self.players:
            player.remove_cards()

    def start_game(self):
        print('---------------------------------------------')
        print("Welcome to Bruno Regelo's BLACKJACK CASINO!!!")
        print('---------------------------------------------')
        self.create_players()
        print('-------------------------')
        while len(self.players) > 0:
            self._play_round() 
            print('Thank you!')
            print('-------------------------')
        print('Come back again soon!')


# Set up game
blackjack_game = Game(2, 6)
blackjack_game.start_game()

        