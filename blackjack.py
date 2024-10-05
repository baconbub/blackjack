"""
Game Name: Blackjack
Description: Player is dealt cards trying to get closer to 21 than the dealer without going over!
Author: Zachary Coe
Date: 2024-10-02
"""


import random



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
D_STARTING_CHIPS = 1000
P_STARTING_CHIPS = 100
SUITS = [CLUB, DIAMOND, HEART, SPADE]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VAL_DICT = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
FACE_VALUE = 10
TWENTYONE = 21
ACE_DIFF = 10
DEALER_LIMIT = 17



def main():
    # How to play
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
    dealer_chips = D_STARTING_CHIPS
    player_chips = P_STARTING_CHIPS
    print_money(dealer_chips, player_chips)
    while True:
        player_bet = get_bet(player_chips)
        double_down = False

        # Deal out intial hands
        dealer_hand = initial_deal(deal_card(SUITS, VALUES))
        player_hand = initial_deal(deal_card(SUITS, VALUES), deal_card(SUITS, VALUES))
        print_both_hands(dealer_hand, player_hand)

        # Check for blackjack
        result = check_end_condition(blackjack(player_hand), "BLACKJACK! You win!", dealer_chips, player_chips, player_bet, dealer_hand, player_hand)
        if result == "break":
            break
        elif result == "continue":
            continue

        # Player takes their turns
        while not bust(player_hand):
            player_choice = player_decision(player_hand, double_down)
            if player_choice == "s":
                break
            elif player_choice == "h":
                player_hand = hit_me(player_hand)
                print_both_hands(dealer_hand, player_hand)
            elif player_choice == "d":
                player_bet *= 2
                double_down = True


        # Check if player busted
        result = check_end_condition(bust(player_hand), "You BUSTED! Dealer wins.", dealer_chips, player_chips, player_bet, dealer_hand, player_hand)
        if result == "break":
            break
        elif result == "continue":
            continue

        # Dealer takes their turns
        dealer_hand = dealer_flip(dealer_hand)
        print_both_hands(dealer_hand, player_hand)
        while determine_hand_value(dealer_hand) < DEALER_LIMIT:
            pause()
            dealer_hand = hit_me(dealer_hand)
            print_both_hands(dealer_hand, player_hand)

        # Check if dealer busted
        result = check_end_condition(bust(dealer_hand), "The dealer BUSTED! You win!", dealer_chips, player_chips, player_bet, dealer_hand, player_hand)
        if result == "break":
            break
        elif result == "continue":
            continue
        
        # Print whether you win or lose
        print(determine_winner(dealer_hand, player_hand))

        # Update player/dealer money
        dealer_chips, player_chips = update_and_print_money(dealer_chips, player_chips, player_bet, dealer_hand, player_hand)
        print_money(dealer_chips, player_chips)

        # Check if player wants to play again
        if not play_again():
            break

    print("Thanks for playing!")
    if player_chips > P_STARTING_CHIPS:
        print(f"You made ${player_chips - P_STARTING_CHIPS}!")
    elif player_chips < P_STARTING_CHIPS:
        print(f"Aww, you lost ${P_STARTING_CHIPS - player_chips}.")



# FUNCTIONS:        

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


def update_and_print_money(dealer_money, player_money, bet, dealer_hand, player_hand):
    if bust(dealer_hand):
        dealer_money -= bet
        player_money += bet
    elif bust(player_hand):
        dealer_money += bet
        player_money -= bet
    else:
        who_won = determine_winner(dealer_hand, player_hand)
        if who_won == "You win!":
            dealer_money -= bet
            player_money += bet
        elif who_won == "Sorry, dealer wins.":
            dealer_money += bet
            player_money -= bet

    # print_money(dealer_money, player_money)
    return dealer_money, player_money


def print_money(dealer_money, player_money):
    print(f"Dealer money: ${dealer_money}\nPlayer money: ${player_money}\n")


def get_bet(current_money):
    while True:     
        try:   
            bet = int(input("How much would you like to bet? "))
            if 0 < bet < current_money:
                return bet
            else:
                raise ValueError()
        except ValueError:
            print(f"Please bet between 0 and {current_money}")


def deal_card(suits, values):
    card = {
        "value": random.choice(values),
         "suit": random.choice(suits)
         }
    
    return card


# Turns the stored values of the cards into
# a visual/printable format
# Helper function for print_cards()
def convert_cards(list_of_cards):
    converted_cards = []
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
        converted_cards.append(card_design)

    return converted_cards


# Takes the visual format of the cards
# and prints them line by line
def print_cards(list_of_cards):
    card_lines = []
    num_of_cards = len(list_of_cards)
    for card in convert_cards(list_of_cards):
        card_lines.append(card.split("\n"))
    for i in range(len(card_lines[0])):
        for j in range(num_of_cards):
            print(card_lines[j][i], end=" ")
        print()


def print_both_hands(dealer_cards, player_cards):
    # Start w/ dealer
    print("\nDealer's hand:")
    print_cards(dealer_cards)
    # Player next
    print("Your hand:")
    print_cards(player_cards)
    

def initial_deal(card2, card1=BLANK_CARD):
    cards = [card1, card2]
    return cards


def determine_hand_value(hand_of_cards):
    hand_value = 0
    aces = 0
    for card in hand_of_cards:
        if isinstance(card, dict):
            value = card["value"]
            hand_value += VAL_DICT[value]
            if value == "A":
                aces += 1

    while hand_value > TWENTYONE and aces:
        hand_value -= ACE_DIFF
        aces -= 1

    return hand_value

# Determines what the player's options
# are and gives a proper list of choices,
# then returns the choice the player made
def player_decision(cards, double_down):
    value_of_hand = determine_hand_value(cards)
    while True:
        try:
            if len(cards) == 2 and 9 <= value_of_hand <= 11 and not double_down:
                choice = input("(H)it, (S)tand, or (D)ouble Down? ").lower()
                choices = ["h", "s", "d"]
                if choice in choices:
                    return choice
                else:
                    raise ValueError()
            elif is_pair(cards) and value_of_hand == 10 and not double_down:
                choice = input("(H)it, (S)tand, (Sp)lit, or (D)ouble Down? ").lower()
                choices = ["h", "s", "d", "sp"]
                if choice in choices:
                    return choice
                else:
                    raise ValueError()
            elif is_pair(cards):
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
    

# Helper function of player_decision()
def is_pair(hand_of_cards):
    if len(hand_of_cards) != 2:
        return False
    card_values = []
    for card in hand_of_cards:
        # Failsafe for if you get a blackjack
        # and BLANKCARD is checked for pair
        if isinstance(card, dict):
            card_values.append(card["value"])
    if len(hand_of_cards) == 2 and card_values[0] == card_values[1]:
        return True
    return False

def hit_me(hand_of_cards):
    cards = hand_of_cards
    cards.append(deal_card(SUITS, VALUES))
    return cards


def dealer_flip(dealer_cards_preflip):
    dealer_hand = [deal_card(SUITS, VALUES), dealer_cards_preflip[1]]
    return dealer_hand


def pause():
    while True:
        input("Press ENTER to continue")
        break

# bust???
def bust(player_hand):
    if determine_hand_value(player_hand) > TWENTYONE:
        return True
    return False


def blackjack(player_hands):
    if determine_hand_value(player_hands) == TWENTYONE:
        return True
    return False


def determine_winner(dealer_hand, player_hand):
    dealer_score = determine_hand_value(dealer_hand)
    player_score = determine_hand_value(player_hand)
    if player_score > dealer_score:
        return "You win!"
    elif dealer_score > player_score:
        return "Sorry, dealer wins."
    else:
        return "You tied!"
    

def check_end_condition(condition, message, dealer_money, player_money, bet, dealer_hand, player_hand):
    if condition:
        print(message)
        dealer_money, player_money = update_and_print_money(dealer_money, player_money, bet, dealer_hand, player_hand)
        print_money(dealer_money, player_money)
        if not play_again():
            return "break"
        return "continue"
    return None



if __name__ == "__main__":
	main()