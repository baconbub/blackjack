"""
Game Name: Blackjack
Description: Player is dealt cards trying to get closer to 21 than the dealer without going over!
Author: Zachary Coe
Date: 2024-10-04
"""



import random



CLUB = "♣"
DIAMOND = "♦"
HEART = "♥"
SPADE = "♠"
D_STARTING_CHIPS = 1000
P_STARTING_CHIPS = 100
SUITS = {CLUB, DIAMOND, HEART, SPADE}
VALUES = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
VAL_DICT = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
FACE_VALUE = 10
TWENTYONE = 21
ACE_DIFF = 10
DEALER_LIMIT = 17



class Card:
    def __init__(self, value, suit, facedown=False):
        self.value = value
        self.suit = suit
        self.facedown = facedown
        if facedown:
            self.appearance = """
 ___ 
|## |
|###|
|_##|
"""
        else:
            self.appearance = f"""
 ___ 
|{self.value} |
| {self.suit} |
|_{self.value}|
"""
    def get_value(self):
        return self.value
        

class Player:
    def __init__(self, money):
        self.money = money
        self.hand_of_cards = []

    def deal_card(self, facedown=False):
        card = Card(random.choice(VALUES), random.choice(SUITS), facedown)
        self.hand_of_cards.append(card)

    def set_new_hand(self):
        self.hand_of_cards = []
        self.deal_card()
        self.deal_card()

    def get_hand(self):
        return self.hand_of_cards
    
    def calculate_hand_value(self):
        hand_value = 0
        aces = 0
        # Calculates hand value
        for card in self.get_hand():
            if isinstance(card, Card):
                value = card.get_value()
                hand_value += VAL_DICT[value]
            # Track number of aces
                if value == "A":
                    aces += 1
        # Adjusts if player goes above 21 and has aces
        while hand_value > TWENTYONE and aces:
            hand_value -= ACE_DIFF
            aces -= 1

        return hand_value
    
    def set_hand_value(self):
        self.hand_value = self.calculate_hand_value()

    def get_hand_value(self):
        return self.hand_value
    
    def bust(self):
        if self.get_hand_value() > TWENTYONE:
            return True
        return False
    
    def blackjack(self):
        if self.get_hand_value() == TWENTYONE:
            return True
        return False


class Dealer(Player):
    def __init__(self, money):
        super().__init__(money)
        
    def set_new_hand(self):
        self.hand_of_cards = []
        self.deal_card(True)
        self.deal_card()


class Game:
    def __init__(self, dealer, player):
        pass


def main():

    print("              Blackjack!")
    instructions = """
Your goal is to gain chips by beating
the dealer in hands of blackjack. You
win by hitting 21 or getting closer to
21 than the dealer. Jacks, Queens, and
Kings are worth 10. Aces are worth either
1 or 11. Every other card is worth the
printed value. Good luck!
"""
    print(instructions)
    player = Player(P_STARTING_CHIPS)
    dealer = Dealer(D_STARTING_CHIPS)
    


def pause():
    while True:
        input("Press ENTER to continue")
        break