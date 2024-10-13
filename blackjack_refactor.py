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
P_STARTING_CHIPS = 250
SUITS = [CLUB, DIAMOND, HEART, SPADE]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VAL_DICT = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
TWENTYONE = 21
ACE_DIFF = 10
DEALER_LIMIT = 17
ACE = "A"
HIT = "h"
STAND = "s"
DOUBLE_DOWN = "d"
SPLIT = "sp"



class Card:
    def __init__(self, value, suit, facedown=True, next_card=None):
        self.value = value
        self.suit = suit
        self.facedown = facedown
        self.next_card = next_card
        self.appearance = self.generate_appearance()

    def generate_appearance(self):
        if self.facedown:
            return """
 ___ 
|## |
|###|
|_##|
"""
        else:
            if self.value == "10":
                return f"""
 ___ 
|{self.value} |
| {self.suit} |
|_{self.value}|
"""
            else:
                return f"""
 ___ 
|{self.value}  |
| {self.suit} |
|__{self.value}|
"""
    
    def flip_card(self):
        self.facedown = False
        self.appearance = self.generate_appearance()

    def set_next_card(self, next_card):
        self.next_card = next_card
        


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
    
    def add_card(self, card: Card):
        self.cards.append(card)
        self.set_hand_value()

    def set_hand_value(self):
        self.value = self.calculate_hand_value()

    def calculate_hand_value(self):
        hand_value = 0
        aces = 0
        # Calculates hand value
        for card in self.cards:
            if isinstance(card, Card):
                value = card.value
                hand_value += VAL_DICT[value]
            # Track number of aces
                if value == ACE:
                    aces += 1
        # Adjusts if player goes above 21 and has aces
        while hand_value > TWENTYONE and aces:
            hand_value -= ACE_DIFF
            aces -= 1

        return hand_value
    
    def bust(self):
        return self.value > TWENTYONE
    
    def blackjack(self):
        return self.value == TWENTYONE
    
    def is_pair(self):
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

    def has_aces(self):
        return any(card.value == ACE for card in self.cards)

    def can_double_down(self):
        return 9 <= self.value <= 11 and self.has_aces() == 0



class Deck:
    def __init__(self):
        self.discard_pile = self.create_discard_pile()
        self.top_card = None
        self.size = 0
        self.shuffle()
        
    def create_discard_pile(self):
        # Initiates all cards into list
        discard_pile = []
        for suit in SUITS:
            for value in VALUES:
                discard_pile.append(Card(value, suit))
        return discard_pile
    
    def shuffle(self):
        self.top_card = None
        random.shuffle(self.discard_pile)
        while self.discard_pile:
            card = self.discard_pile.pop(0)
            card.set_next_card(self.top_card)
            self.top_card = card
            self.size += 1

    def draw_card(self) -> Card:
        if self.size > 0:
            card_being_dealt = self.top_card
            self.top_card = card_being_dealt.next_card
            card_being_dealt.set_next_card(None)
            self.size -= 1
            return card_being_dealt
        elif self.size == 0:
            print("\nOut of cards, shuffling deck.\n")
            self.shuffle()
            return self.draw_card()



class Player:
    def __init__(self, money):
        self.money = money
        self.hands = []
        self.bankrupt = False

    # TEST METHOD FOR CHECKING DOUBLE DOWN AND SPLIT
    # def test_deal_card(self):
    #     card = Card("5", DIAMOND, False)
    #     self.hands[0].add_card(card)
    # TEST METHOD FOR CHECKING DOUBLE DOWN AND SPLIT

    def deal_card(self, deck: Deck, hand_index=0):
        card = deck.draw_card()
        card.flip_card()
        self.hands[hand_index].add_card(card)

    def discard_cards(self, deck: Deck, hand_index=0):
        # print("Discarding cards.")
        for card in self.hands[hand_index].cards:
            deck.discard_pile.append(card)

    def start_new_hand(self, deck: Deck):
        self.hands = [Hand()]
        self.deal_card(deck)
        self.deal_card(deck)
    
    def win_bet(self, bet):
        self.money += bet

    def lose_bet(self, bet):
        self.money -= bet

    def set_bankrupt(self):
        if self.money <= 0:
            self.bankrupt = True
        else: 
            self.bankrupt = False

    def can_increase_bet(self, bet):
        return (bet * 2) <= self.money

    def take_turn(self, hand: Hand, bet):
        while True:
            try:
                if self.can_increase_bet(bet) and hand.is_pair()  and hand.can_double_down():
                    choice = input("(H)it, (S)tand, (Sp)lit, or (D)ouble Down? ").lower()
                    choices = [HIT, STAND, DOUBLE_DOWN, SPLIT]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                elif self.can_increase_bet(bet) and hand.can_double_down():
                    choice = input("(H)it, (S)tand, or (D)ouble Down? ").lower()
                    choices = [HIT, STAND, DOUBLE_DOWN]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                elif self.can_increase_bet(bet)and hand.is_pair():
                    choice = input("(H)it, (S)tand, or (Sp)lit? ").lower()
                    choices = [HIT, STAND, SPLIT]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
                else:
                    choice = input("(H)it or (S)tand? ").lower()
                    choices = [HIT, STAND]
                    if choice in choices:
                        return choice
                    else:
                        raise ValueError()
            except ValueError:
                print(f"Please input one of the letters in parentheses.")

    def split_hand(self, deck: Deck, hand_index):
        # Make new hand
        new_hand = Hand()
        # Move 1 from pair to new hand
        new_card = self.hands[hand_index].cards.pop()
        new_hand.add_card(new_card)
        # Assign hand to player
        self.hands.append(new_hand)
        # Deal card to each of two new hands
        self.deal_card(deck, hand_index)
        self.deal_card(deck, (len(self.hands) - 1))



class Dealer(Player):
    def __init__(self, money):
        super().__init__(money)

    def deal_facedown_card(self, deck: Deck, hand_index=0):
        card = deck.draw_card()
        self.hands[hand_index].add_card(card)
        
    def start_new_hand(self, deck: Deck):
        self.hands = [Hand()]
        self.deal_facedown_card(deck)
        self.deal_card(deck)

    def take_turn(self, deck: Deck):
        pause()
        self.deal_card(deck)



class Game:
    def __init__(self, dealer: Dealer, player: Player, deck: Deck, intro: str):
        self.dealer = dealer
        self.player = player
        self.deck = deck
        self.play_again = True
        self.hand_winners = []
        self.bet = 0
        print(intro)

    def print_money(self):
        print(f"Dealer money: ${self.dealer.money}\nPlayer money: ${self.player.money}\n")

    def get_bet(self):
        while True:     
            try:   
                bet = int(input(f"How much would you like to bet? (1 - {self.player.money}) "))
                if 0 < bet <= self.player.money:
                    return bet
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please input a bet between 0 and {self.player.money}")
    
    def get_dealer_hand(self):
        # Dealer only ever has one hand
        return self.dealer.hands[0]

    def print_cards(self, hand_of_cards):
        card_lines = []
        num_of_cards = len(hand_of_cards)
        for card in hand_of_cards:
            if isinstance(card, Card):
                card_lines.append(card.appearance.split("\n"))
        for i in range(len(card_lines[0])):
            for j in range(num_of_cards):
                print(card_lines[j][i], end=" ")
            print()
    
    def print_all_hands(self):
        # Dealer first
        if self.get_dealer_hand().cards[0].facedown == True:
            print(f"\nDealer's hand: {VAL_DICT[self.get_dealer_hand().cards[1].value]}", end="")
            self.print_cards(self.dealer.hands[0].cards)
        else:
            print(f"\nDealer's hand: {self.get_dealer_hand().value}", end="")
            self.print_cards(self.dealer.hands[0].cards)
        # Player next
        if len(self.player.hands) == 1:
            print(f"Your hand: {self.player.hands[0].value}", end="")
            self.print_cards(self.player.hands[0].cards)
        else:
            for index, hand in enumerate(self.player.hands, start=1):
                print(f"Hand #{index}: {hand.value}", end="")
                self.print_cards(hand.cards)

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
    
    def update_money(self, current_hand_idx):
        hand_winner = self.hand_winners[current_hand_idx]
        if hand_winner == "player":
            self.player.win_bet(self.bet)
            self.dealer.lose_bet(self.bet)
        elif hand_winner == "dealer":
            self.player.lose_bet(self.bet)
            self.dealer.win_bet(self.bet)
    
    def set_hand_winners(self, current_hand_idx):
        player_hand = self.player.hands[current_hand_idx]
        dealer_hand = self.get_dealer_hand()

        if player_hand.bust() and dealer_hand.bust():
            self.hand_winners.append("dealer")
        elif player_hand.bust():
            self.hand_winners.append("dealer")
        elif dealer_hand.bust():
            self.hand_winners.append("player")
        else:
            if player_hand.value > self.get_dealer_hand().value:
                self.hand_winners.append("player")
            elif self.get_dealer_hand().value > player_hand.value:
                self.hand_winners.append("dealer")
            else:
                self.hand_winners.append(None)
            
    def start_round(self):
        self.bet = self.get_bet()
        self.hand_winners = []
        self.dealer.start_new_hand(self.deck)
        self.player.start_new_hand(self.deck)
        self.print_all_hands()
        
    def end_round(self):
        current_hand = 0
        while current_hand < len(self.player.hands):
            self.set_hand_winners(current_hand)
            self.print_winner_message(current_hand)
            self.update_money(current_hand)
            self.print_money()
            self.player.discard_cards(self.deck, current_hand)
            current_hand += 1

        if self.is_bankrupt():
            self.play_again = False
            return

        self.set_play_again()

    def print_winner_message(self, current_hand_idx):
        hand_winner = self.hand_winners[current_hand_idx]
        player_hand = self.player.hands[current_hand_idx]

        if len(self.player.hands) == 1:
            if hand_winner == "player":
                print("You win!")
            elif hand_winner == "dealer":
                print("Sorry, the dealer wins.")
            elif hand_winner is None and not player_hand.bust() and not self.get_dealer_hand().bust():
                print("You tied!")
        else:
            if hand_winner == "player":
                print(f"\nHand #{current_hand_idx + 1} wins!")
            elif hand_winner == "dealer":
                print(f"\nHand #{current_hand_idx + 1} loses.")
            elif hand_winner is None and not player_hand.bust() and not self.get_dealer_hand().bust():
                print(f"\nHand #{current_hand_idx + 1} tied!")
    
    def player_turn(self):
        current_hand = 0
        while current_hand < len(self.player.hands):
            hand = self.player.hands[current_hand]

            if len(self.player.hands) > 1:
                    print(f"\nPlaying Hand #{current_hand + 1}") 
            
            while not hand.bust():                    
                player_choice = self.player.take_turn(hand, self.bet)
                if player_choice == STAND:
                    current_hand += 1
                    break
                elif player_choice == HIT:
                    self.player.deal_card(self.deck, current_hand)
                    self.print_all_hands()
                elif player_choice == DOUBLE_DOWN:
                    self.bet *= 2
                    self.player.deal_card(self.deck, current_hand)
                    self.print_all_hands()
                    current_hand += 1
                    break
                elif player_choice == SPLIT:
                    self.player.split_hand(self.deck, current_hand)
                    self.print_all_hands()
                    break

            if hand.bust():
                if len(self.player.hands) == 1:
                    print("You BUSTED!")
                    return True
                else:
                    print(f"Hand #{current_hand + 1} BUSTED!")
                    current_hand += 1

        return False
    
    def dealer_turn(self):
        card1 = self.get_dealer_hand().cards[0]
        card1.flip_card()
        self.print_all_hands()
        while self.get_dealer_hand().value < DEALER_LIMIT:
            self.dealer.take_turn(self.deck)
            self.print_all_hands()

    def update_bankrupt(self):
        self.dealer.set_bankrupt()
        self.player.set_bankrupt()

    def is_bankrupt(self):
        self.update_bankrupt()
        return self.player.bankrupt or self.dealer.bankrupt
        
    def end_game(self):
        if self.dealer.bankrupt:
            print("The dealer ran out of money!")
        elif self.player.bankrupt:
            print("You ran out of chips!")
        print("Thanks for playing!")
        if self.player.money > P_STARTING_CHIPS:
            print(f"You made ${self.player.money - P_STARTING_CHIPS}!")
        elif self.player.money < P_STARTING_CHIPS:
            print(f"Sorry, you lost ${P_STARTING_CHIPS - self.player.money}.")



def main():
    # Start game
    instructions = """
             Blackjack!
Your goal is to gain chips by beating
the dealer in hands of blackjack. You
win by hitting 21 or getting closer to
21 than the dealer. Ties go to the
dealer. 

- Jacks, Queens, and Kings are worth 10.
- Aces are worth either 1 or 11.
- Every other card is worth the printed 
  value.

Hit: Add a card to your hand
Stand: Keep your hand
Double Down: Double your bet and only 
             gain one more card
Split: Create two separate hands with
       each of your cards, making a
       new bet for each hand.

              Good luck!
"""
    player = Player(P_STARTING_CHIPS)
    dealer = Dealer(D_STARTING_CHIPS)
    deck = Deck()
    blackjack = Game(dealer, player, deck, instructions)
    blackjack.print_money()

    while blackjack.play_again:

        # Deal initial hands
        blackjack.start_round()

        # Check for blackjack (blackjack only works on first hand)
        if blackjack.player.hands[0].blackjack():
            print("BLACKJACK!")
            blackjack.end_round()
            if not blackjack.play_again:
                break
            continue
        
        # Loops till player finishes their turn
        player_busted = blackjack.player_turn()

        # If bankrupt, end the round then game
        if blackjack.is_bankrupt():
            blackjack.end_round()
            break
        
        # if the player busts w/ 1 hand, end round
        if player_busted:
            blackjack.end_round()
            continue

        # Loops till dealer finishes their turn
        blackjack.dealer_turn()

        # Check for dealer bust
        if blackjack.get_dealer_hand().bust():
            print("The dealer BUSTED!")
            
        # End of round cleanup
        blackjack.end_round()

        # Check if player wants to play another round
        if not blackjack.play_again or blackjack.is_bankrupt():
            break
    
    # Concludes game by printing final money values
    blackjack.end_game()



def pause():
    while True:
        input("Press ENTER to continue")
        break



if __name__ == "__main__":
	main()