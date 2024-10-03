"""
Game Name: Blackjack
Description: Player is dealt cards trying to get closer to 21 than the dealer without going over!
Author: Zachary Coe
Date: 2024-10-02
"""


import random



# Rules of blackjack
# Choose to make bet
# Dealer serves to me, themself, me, themself(face down)
# Hit, Double, Stand, Split?
# if stand, dealer reveals card, and plays to standard casino rules
# if hit, go till stand or till 21 or till bust

BLANK_CARD = """
 ___ 
|## |
|###|
|_##|
"""
CLUB = "♣"
DIAMOND = "♦"
HEART = "♥"
SPADE = "♠"
STARTING_GOLD = 1000
SUITS = [CLUB, DIAMOND, HEART, SPADE]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def main():
    # How to play
    print("        Welcome to blackjack!")
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

    while play_again():
        
        dealer_hand = initial_dealer_deal(choose_card(SUITS, VALUES))
        player_hand = []

        
        initial_player_deal(choose_card(SUITS, VALUES), choose_card(SUITS, VALUES))

        # while player_hit():
        #     player_deal()
        #     player_hit()

        # dealer_flip()
        # dealer_deal()

        # decide_winner()
        # play_again()
        # get_bet()


def play_again():
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


def get_bet():
    print(f"Player: {STARTING_GOLD}")
    while True:     
        try:   
            bet = input("How much would you like to bet? ")
            if 0 < bet < STARTING_GOLD:
                return bet
            else:
                raise ValueError()
        except ValueError:
            print(f"Please bet between 0 and {STARTING_GOLD}")


def choose_card(suits, values):
    value = random.choice(values)
    suit = random.choice(suits)
    card_design = f"""
 ___
|{value}  |
| {suit} |
|__{value}|
"""
    return card_design


def initial_dealer_deal(dealer_card2):
    cards = [BLANK_CARD, dealer_card2]
    
    card1_lines = BLANK_CARD.split("\n")
    card2_lines = dealer_card2.split("\n")

    print("\nDealer's hand:", end="")
    for i in range(len(card1_lines)):
        print(f"{card1_lines[i]} {card2_lines[i]}")

    return cards





def initial_player_deal(player_card1, player_card2):
    return


if __name__ == "__main__":
	main()