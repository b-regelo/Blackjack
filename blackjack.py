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
        elif bet < self.balance:
            print(f'Your balance is only {self.balance}!')
            bet = self.balance
        
        self.balance -= bet
        return bet
            
    def receive_winnings(self, value):
        self.balance += value

    def check_balance(self):
        return self.balance
        
    