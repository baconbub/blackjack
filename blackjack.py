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
D_STARTING_GOLD = 1000
P_STARTING_GOLD = 100
SUITS = [CLUB, DIAMOND, HEART, SPADE]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
FACE_VALUE = 10
TWENTYONE = 21
ACE_ELEVEN = 11
ACE_ONE = 1

def main():
    # How to play
    print("            Welcome to blackjack!")
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
    dealer_gold = D_STARTING_GOLD
    player_gold = P_STARTING_GOLD
    while True:
        
        player_bet = get_bet(player_gold)

        dealer_hand = initial_dealer_deal(choose_card(SUITS, VALUES))
        player_hand = initial_player_deal(choose_card(SUITS, VALUES), choose_card(SUITS, VALUES))

        # print(determine_hand_value(player_hand))
        # while player_hit():
        #     player_deal()
        #     player_hit()

        # dealer_flip()
        # dealer_deal()

        # decide_winner()
        # play_again()
        # get_bet()


        if not play_again():
            break

    print("Thanks for playing!")
    if player_gold > P_STARTING_GOLD:
        print(f"You made {player_gold - P_STARTING_GOLD} money!")
    elif player_gold < P_STARTING_GOLD:
        print(f"Aww, you lost {P_STARTING_GOLD - player_gold} money.")

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


def get_bet(money):
    print(f"Player: ${money}")
    while True:     
        try:   
            bet = int(input("How much would you like to bet? "))
            if 0 < bet < money:
                return bet
            else:
                raise ValueError()
        except ValueError:
            print(f"Please bet between 0 and {money}")


def choose_card(suits, values):
    card = {
        "value": random.choice(values),
         "suit": random.choice(suits)
         }
    
    # value = random.choice(values)
    # suit = random.choice(suits)
    
    return card


# Turns the stored values of the cards into
# a visual/printable format
def create_cards(list_of_cards):
    created_cards = []
    for card in list_of_cards:
        if card == BLANK_CARD:
            card_design = BLANK_CARD
        else:
            value = card["value"]
            suit = card["suit"]
            if value == "10":
                card_design = f"""
 ___ 
|{value} |
| {suit} |
|_{value}|
"""
            else:
                card_design = f"""
 ___ 
|{value}  |
| {suit} |
|__{value}|
"""
        created_cards.append(card_design)

    return created_cards


# Takes the visual format of the cards
# and prints them line by line
def print_cards(list_of_cards):
    card_lines = []
    num_of_cards = len(list_of_cards)
    for card in list_of_cards:
        card_lines.append(card.split("\n"))
    for i in range(len(card_lines[0])):
        for j in range(num_of_cards):
            print(card_lines[j][i], end=" ")
        print()


def initial_dealer_deal(dealer_card2):
    cards = [BLANK_CARD, dealer_card2]

    print("\nDealer's hand:", end="")
    print_cards(create_cards(cards))

    return cards


def initial_player_deal(player_card1, player_card2):
    cards = [player_card1, player_card2]

    print("Your hand:", end="")
    print_cards(create_cards(cards))

    return cards


def determine_hand_value(hand_of_cards):
    card_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    hand_value = 0
    aces = 0
    for card in hand_of_cards:
        value = card["value"]
        hand_value += card_values[value]
        if value == "A":
            aces += 1

    while hand_value > 21 and aces:
        hand_value -= 10
        aces -= 1

    return hand_value

# Determines what the player's options
# are and gives a proper list of choices,
# then returns the choice the player made
def player_decision(value_of_hand, cards):
    while True
        try:
            if len(cards) == 2 and 9 <= value_of_hand <= 11:
                choice = input("(H)it, (S)tand, or (D)ouble Down? ").lower()
                choices = ["h", "s", "d"]
                if choice == choices:
                    return choice
                else:
                    raise ValueError()
            elif is_pair(cards) and value_of_hand == 10:
                choice = input("(H)it, (S)tand, (Sp)lit, or (D)ouble Down? ").lower()
                choices = ["h", "s", "d", "sp"]
                if choice == choices:
                    return choice
                else:
                    raise ValueError()
            elif is_pair(cards):
                choice = input("(H)it, (S)tand, or (Sp)lit? ").lower()
                choices = ["h", "s", "sp"]
                if choice == choices:
                    return choice
                else:
                    raise ValueError()
            else:
                choice = input("(H)it or (S)tand? ")
                choices = ["h", "s"]
                if choice == choices:
                    return choice
                else:
                    raise ValueError()        
        except ValueError:
                print(f"Please input one of the letters in parentheses.")
    
# Helper function of player_decision()
def is_pair(hand_of_cards):
    card_values = []
    if len(hand_of_cards) == 2:
        for card in hand_of_cards:
            card_values.append(card["value"])
    if card_values[0] == card_values[1]:
        return True
    return False



if __name__ == "__main__":
	main()