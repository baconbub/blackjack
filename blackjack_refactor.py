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
SUITS = [CLUB, DIAMOND, HEART, SPADE]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
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
            if self.value == "10":
                self.appearance = f"""
 ___ 
|{self.value} |
| {self.suit} |
|_{self.value}|
"""
            else:
                self.appearance = f"""
 ___ 
|{value}  |
| {suit} |
|__{value}|
"""
                
    def get_value(self):
        return self.value
    
    def get_appearance(self):
        return self.appearance
    
    def flip_card(self):
        self.facedown = False
        if self.value == "10":
                self.appearance = f"""
 ___ 
|{self.value} |
| {self.suit} |
|_{self.value}|
"""
            else:
                self.appearance = f"""
 ___ 
|{value}  |
| {suit} |
|__{value}|
"""
        


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
    
    def get_money(self):
        return self.money
    
    def win_bet(self, bet):
        self.money += bet

    def lose_bet(self, bet):
        self.money -= bet
    
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
    def __init__(self, dealer: Dealer, player: Player, intro: str):
        self.dealer = dealer
        self.player = player
        self.play_again = True
        print(intro)

    def print_money(self):
        print(f"Dealer money: ${self.dealer.get_money()}\nPlayer money: ${self.player.get_money()}")

    def get_bet(self):
        while True:     
            try:   
                bet = int(input("How much would you like to bet? "))
                if 0 < bet < self.player.get_money():
                    return bet
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please bet between 0 and {self.player.get_money()}")

    def print_cards(self, player: Player):
        card_lines = []
        num_of_cards = len(player.get_hand())
        for card in player.get_hand():
            if isinstance(card, Card):
                card_lines.append(card.get_appearance().split("\n"))
        for i in range(len(card_lines[0])):
            for j in range(num_of_cards):
                print(card_lines[j][i], end=" ")
            print()
    
    def print_both_hands(self):
        # Dealer first
        print("\nDealer's hand:")
        self.print_cards(self.dealer)
        # Player next
        print("Your hand:")
        self.print_cards(self.player)

    def set_play_again(self):
        play_list = ["n", "y"]
        while True:     
            try:   
                play = input("Play again? (y/n) ").lower()
                if play in play_list:
                    if play == "y":
                        return True
                    else:
                        return False
                else:
                    raise ValueError()
            except ValueError:
                print("Please type either y or n.")

    def get_play_again(self):
        return self.play_again



def main():
    # Start game
    instructions = """
             Blackjack!
Your goal is to gain chips by beating
the dealer in hands of blackjack. You
win by hitting 21 or getting closer to
21 than the dealer. Jacks, Queens, and
Kings are worth 10. Aces are worth either
1 or 11. Every other card is worth the
printed value. Good luck!
"""
    player = Player(P_STARTING_CHIPS)
    dealer = Dealer(D_STARTING_CHIPS)
    blackjack = Game(dealer, player, instructions)
    blackjack.print_money()

    while blackjack.get_play_again():
        player_bet = blackjack.get_bet()
        # double_down = False

        # Deal initial hands
        player.set_new_hand()
        dealer.set_new_hand()
        blackjack.print_both_hands()

        # Check for blackjack
        if player.blackjack():
            print("BLACKJACK! You win!")
            player.win_bet(player_bet)
            dealer.lose_bet(player_bet)
            if not blackjack.set_play_again():
                break
            continue



def pause():
    while True:
        input("Press ENTER to continue")
        break



if __name__ == "__main__":
	main()