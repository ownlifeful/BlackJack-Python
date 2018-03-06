#!/usr/bin/env python

# BlackJack

# You need to create a simple text-based BlackJack game
# The game needs to have one player versus an automated dealer.
# The player can stand or hit.
# The player must be able to pick their betting amount.
# You need to keep track of the player's total money.

import random

class Card:
    def __init__(self,suite,rank):
        self.suite = suite
        self.rank = rank

    def __str__(self):
        if self.rank == 0:
            rank = "A"
        elif self.rank < 10:
            rank = str(self.rank + 1)
        else:
            ranks = ["J", "Q", "K"]
            rank = ranks[ self.rank - 10 ]

        suites = ["\u2665", "\u2660", "\u2666", "\u2663"]
        suite = suites[ self.suite ]

        return rank + suite

###############################################################################

class Deck:
    cards = []

    def __init__(self):
        for suite in range(0,4):
            for rank in range(0,13):
                self.cards.append( Card(suite,rank) )

    def shuffle(self):
        random.shuffle(self.cards)

    def output(self):
        for card in self.cards:
            print(card)

    def get_next_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("The deck is empty.")

###############################################################################

class Player:

    def __init__(self):
        self.hand = []

    def take_card(self,card):
        self.hand.append(card)

    def throw_hand(self):
        self.hand = []

    def show_stats(self):
        print ("\t" + ("-" * 60))
        print ("\tWho: ", self.name )
        print ("\tHand:", " ".join([ str(x) for x in self.hand]))
        print ("\tScore: %d" %(self.score()))
        # print ("=" * 60)

    def score(self):
        score = 0
        ace_count = 0
        for card in self.hand:
            if card.rank == 0:
                score += 11 # Counting Ace as 11
                ace_count += 1
            elif card.rank <= 9:
                score += card.rank + 1
            else:
                score += 10 # Face cards

        if score > 21 and ace_count > 0:
            for x in range(0,ace_count):
                score -= 10 # Counting Ace as 1
                if score <= 21:
                    break
        return score

###############################################################################

class HumanPlayer(Player):
    name = "You"

    def __init__(self,init_amount=10000.):
        super().__init__()
        self.balance = init_amount

    def show_stats(self):
        super().show_stats()
        print ("\tBalance: $%5.2f" %(self.balance))

    def add_balance(self,add_amount):
        self.balance += add_amount

    def reduce_balance(self, reduce_amount):
        self.balance -= reduce_amount

    def get_bet(self):
        get_input = True
        while get_input:
            get_input = False
            print ("You have $%5.2f" %( self.balance ))
            try:
                bet = abs(float(input("How much would you like to bet? ")))
            except:
                print("Whoops. Something went wrong. Try again.")
                get_input = True
                continue
            if bet > self.balance:
                print ("You cannot bet $%5.2f, as you only have $%5.2f" %(bet, self.balance))
                get_input = True
        print("Thank you for betting $%5.2f" %(bet))
        return bet

    def get_hit(self):
        while True:
            choice = input("Enter H to hit, S to stand: ")
            if choice == "H" or choice == "h":
                return True
            elif choice == "S" or choice == "s":
                return False
            else:
                print("H and S are the only valid choices.")

###############################################################################

class Dealer(Player):
    name = "Bellagio"

###############################################################################

def get_playing():
    while True:
        choice = input("Play again? Y/N: ")
        if choice == "Y" or choice == "y":
            return True
        elif choice == "N" or choice == "n":
            return False
        else:
            print("Y and N are the only valid choices.")

###############################################################################

player = HumanPlayer()
dealer = Dealer()
playing = True
while playing:
    deck = Deck()
    deck.shuffle()
    deck.output()
    
    bet = player.get_bet()
    player.reduce_balance(bet)

    player.take_card( deck.get_next_card() )
    dealer.take_card( deck.get_next_card() )
    player.take_card( deck.get_next_card() )
    dealer.take_card( deck.get_next_card() )

    player.show_stats()
    dealer.show_stats()

    game_on = True

    if dealer.score() == 21:
        print ("BlackJack! Dealer wins!")
        game_on = False

    if player.score() == 21:
        print ("BlackJack! You win!")
        player.add_balance( bet * 3 )
        game_on = False

    while game_on:
        # Player goes first
        player_took_hit = player.get_hit()
        if player_took_hit:
            card = deck.get_next_card()
            print("You drew: ", card)
            player.take_card(card)
        else:
            print("You chose to stand.")

        player.show_stats()
        player_score = player.score()
        if player_score == 21:
            print ("Winner, winner, chicken dinner! BlackJack!")
            player.add_balance( bet * 3 )
            break
        elif player_score > 21:
            print ("BUST! You lose.")
            break

        # Dealer goes next
        dealer_stands_at = 18 if player_took_hit else player_score

        if dealer.score() >= dealer_stands_at:
            print("Dealer stands.")

        winner_decided = False
        while dealer.score() < dealer_stands_at:
            card = deck.get_next_card()
            print("Dealer drew: ", card)
            dealer.take_card(card)
            dealer.show_stats()
            dealer_score = dealer.score()
            if dealer_score == 21:
                print ("BlackJack! Dealer wins!")
                winner_decided = True
                break
            elif dealer_score > 21:
                print ("Dealer BUST! You win.")
                player.add_balance( bet * 2 )
                winner_decided = True
                break
            if player_took_hit:
                break

        if winner_decided:
            print("We have a winner.")
            break

        if not player_took_hit:
            if ( player.score() > dealer.score() ):
                print ("You scored %d to the dealer's %d. You win!" %( player.score(), dealer.score() ))
                player.add_balance( bet * 2 )
            else:
                print ("You scored %d to the dealer's %d. You lose!" %( player.score(), dealer.score() ))

            break

    player.throw_hand()
    dealer.throw_hand()
    playing = get_playing()
