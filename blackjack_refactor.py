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
|{self.value}  |
| {self.suit} |
|__{self.value}|
"""
    
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
|{self.value}  |
| {self.suit} |
|__{self.value}|
"""
        


class Player:
    def __init__(self, money):
        self.money = money
        self.hand_of_cards = []
        self.bankrupt = False
        self.can_double_down = False

    def deal_card(self, facedown=False):
        card = Card(random.choice(VALUES), random.choice(SUITS), facedown)
        self.hand_of_cards.append(card)
        self.set_hand_value()

    def set_new_hand(self):
        self.double_down = False
        self.hand_of_cards = []
        self.deal_card()
        self.deal_card()
        self.set_hand_value()
    
    def win_bet(self, bet):
        self.money += bet

    def lose_bet(self, bet):
        self.money -= bet
    
    # def check_double_down(self, game: Game):
    #     bet = game.bet
    #     if (bet * 2) <= self.money and len(self.hand_of_cards) == 2 and 9 <= self.hand_value <= 11:
    #         return True
    #     return False

    def calculate_hand_value(self):
        hand_value = 0
        aces = 0
        # Calculates hand value
        for card in self.hand_of_cards:
            if isinstance(card, Card):
                value = card.value
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

    def set_bankrupt(self):
        if self.money <= 0:
            self.bankrupt = True
        else: 
            self.bankrupt = False

    def has_pair(self):
        if len(self.hand_of_cards) != 2:
            return False
        card1, card2 = self.hand_of_cards
        if isinstance(card1, Card) and isinstance(card2, Card) and card1.value == card2.value:
            return True
        return False
    
    def bust(self):
        if self.hand_value > TWENTYONE:
            return True
        return False
    
    def blackjack(self):
        if self.hand_value == TWENTYONE:
            return True
        return False
    
    def take_turn(self):
        while True:
            try:
                if self.can_double_down:
                    choice = input("(H)it, (S)tand, or (D)ouble Down? ").lower()
                    choices = ["h", "s", "d"]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                elif self.has_pair() and self.can_double_down:
                    choice = input("(H)it, (S)tand, (Sp)lit, or (D)ouble Down? ").lower()
                    choices = ["h", "s", "d", "sp"]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                elif self.has_pair():
                    choice = input("(H)it, (S)tand, or (Sp)lit? ").lower()
                    choices = ["h", "s", "sp"]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                else:
                    choice = input("(H)it or (S)tand? ").lower()
                    choices = ["h", "s"]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
            except ValueError:
                print(f"Please input one of the letters in parentheses.")


class Dealer(Player):
    def __init__(self, money):
        super().__init__(money)
        
    def set_new_hand(self):
        self.hand_of_cards = []
        self.deal_card(True)
        self.deal_card()

    def take_turn(self):
        pause()
        self.deal_card()


class Game:
    def __init__(self, dealer: Dealer, player: Player, intro: str):
        self.dealer = dealer
        self.player = player
        self.play_again = True
        self.winner = None
        self.bet = 0
        print(intro)

    def print_money(self):
        print(f"Dealer money: ${self.dealer.money}\nPlayer money: ${self.player.money}")

    def get_bet(self):
        while True:     
            try:   
                bet = int(input("How much would you like to bet? "))
                if 0 < bet <= self.player.money:
                    return bet
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please bet between 0 and {self.player.money}")

    def print_cards(self, player: Player):
        card_lines = []
        num_of_cards = len(player.hand_of_cards)
        for card in player.hand_of_cards:
            if isinstance(card, Card):
                card_lines.append(card.appearance.split("\n"))
        for i in range(len(card_lines[0])):
            for j in range(num_of_cards):
                print(card_lines[j][i], end=" ")
            print()
    
    def print_both_hands(self):
        # Dealer first
        print("\nDealer's hand:", end="")
        self.print_cards(self.dealer)
        # Player next
        print("Your hand:", end="")
        self.print_cards(self.player)

    def set_play_again(self):
        play_list = ["n", "y"]
        while True:     
            try:   
                play = input("Play again? (y/n) ").lower()
                if play in play_list:
                    if play == "y":
                        self.play_again = True
                        return
                    else:
                        self.play_again = False
                        return
                else:
                    raise ValueError()
            except ValueError:
                print("Please type either y or n.")

    def check_end_condition(self, condition, text):
        if condition:
            print(text)
            return True
        return False
    
    def update_money(self):
        winner = self.check_winner()
        if winner is self.player:
            self.player.win_bet(self.bet)
            self.dealer.lose_bet(self.bet)
        elif winner is self.dealer:
            self.player.lose_bet(self.bet)
            self.dealer.win_bet(self.bet)
    
    def check_winner(self):
        if self.dealer.bust():
            return self.player
        elif self.player.bust():
            return self.dealer
        else:
            if self.player.hand_value > self.dealer.hand_value:
                return self.player
            elif self.dealer.hand_value > self.player.hand_value:
                return self.dealer 
            else:
                return None
            
    def set_winner(self):
        self.winner = self.check_winner()
            
    def start_round(self):
        self.bet = self.get_bet()
        self.winner = None
        self.dealer.set_new_hand()
        self.player.set_new_hand()
        self.print_both_hands()
            
    def end_round(self, player_busted=False, dealer_busted=False, blackjack=False):
        if not player_busted and not dealer_busted and not blackjack:
            self.set_winner()
            self.print_winner_message()
        self.update_money()
        self.print_money()
        self.set_play_again()

    def print_winner_message(self):
        if self.winner is self.player:
            print("You win!")
        elif self.winner is self.dealer:
            print("Sorry, the dealer wins.")
        elif self.winner is None and not self.player.bust() and not self.dealer.bust():
            print("You tied!")

    def check_double_down(self):
        if (self.bet * 2) <= self.player.money and len(self.player.hand_of_cards) == 2 and 9 <= self.player.hand_value <= 11:
            self.player.can_double_down = True
        self.player.can_double_down = False
    
    def player_turn(self):
        self.check_double_down()
        while not self.player.bust():
            player_choice = self.player.take_turn()
            if player_choice == "s":
                break
            elif player_choice == "h":
                self.player.deal_card()
                self.print_both_hands()
            elif player_choice == "d":
                self.bet *= 2
                self.player.deal_card()
                self.print_both_hands()
                break
            elif player_choice == "sp":
                continue
    
    def dealer_turn(self):
        card1 = self.dealer.hand_of_cards[0]
        if isinstance(card1, Card) and card1.facedown:
            card1.flip_card()
        self.print_both_hands()
        while self.dealer.hand_value < DEALER_LIMIT:
            self.dealer.take_turn()
            self.print_both_hands()

    def update_bankrupt(self):
        self.dealer.set_bankrupt()
        self.player.set_bankrupt()

    def if_bankrupt(self):
        self.update_bankrupt()
        if self.player.bankrupt or self.dealer.bankrupt:
            return True
        else:
            return False
        
    def end_game(self):
        if self.dealer.bankrupt:
            print("The dealer ran out of money!")
        elif self.player.bankrupt:
            print("You ran out of chips!")
        print("Thanks for playing!")
        if self.player.money > P_STARTING_CHIPS:
            print(f"You made ${self.player.money - P_STARTING_CHIPS}!")
        elif self.player.money <= 0:
            print("You lost all your money!")
        elif self.player.money < P_STARTING_CHIPS:
            print(f"Sorry, you lost ${P_STARTING_CHIPS - self.player.money}.")



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

    while blackjack.play_again:

        # Deal initial hands
        blackjack.start_round()

        # Check for blackjack
        if blackjack.check_end_condition(blackjack.player.blackjack(), "BLACKJACK!"):
            blackjack.end_round(blackjack=True)
            if not blackjack.play_again:
                break
            continue
        
        # Loops till player finishes their turn
        blackjack.player_turn()

        # Check for player bust
        if blackjack.check_end_condition(blackjack.player.bust(), "You BUSTED!"):
            blackjack.end_round(player_busted=True)
            if not blackjack.play_again:
                break
            continue

        # Loops till dealer finishes their turn
        blackjack.dealer_turn()

        # Check for dealer bust
        if blackjack.check_end_condition(blackjack.dealer.bust(), "The dealer BUSTED!"):
            blackjack.end_round(dealer_busted=True)
            if not blackjack.play_again:
                break
            continue

        # End of round cleanup
        blackjack.end_round()

        # Check if player wants to play another round
        if not blackjack.play_again or blackjack.if_bankrupt():
            break
    
    blackjack.end_game()



def pause():
    while True:
        input("Press ENTER to continue")
        break



if __name__ == "__main__":
	main()