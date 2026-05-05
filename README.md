Blackjack Terminal game
Make bets against an AI dealer. Features a 52-card deck with ASCII-style art that shuffles after exhausting all cards.

![image](https://github.com/user-attachments/assets/0c655021-73bb-4631-b915-271ab0cbfb71)

How it works:
The dealer follows standard dealer logic when deciding to hit or stand. 52-card deck is built prior to each session and shuffled after all cards have been played. Game also features 'doubling,' which allows the player to add another hand of cards and place bets on each. 

Features:
- ASCII art cards
- AI opponent
- Dynamic scaling for doubling number of hands
- Betting system

Challenges:
- Dynamic scaling for multiple hands was not possible -> Refactored from a "hand" class that stored your cards together into "hands" class that stored all sets of cards
