import random


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

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


class CardShoe:
    suits = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
    cards = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, number_of_decks):
        self.number_of_decks = number_of_decks
        self.card_shoe = [card + suit for _ in range(number_of_decks)
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



        