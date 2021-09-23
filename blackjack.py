"""
Name: Subin Moon

blackjack.py
"""
import doctest
import random
import itertools


BLACK_JACK = 21
DEALER_LIMIT = 14
MINIMUM_BET = 10
COURT_CARD = 10
TEN_CARD = 10
A_VALUE = 10
INIT_MONEY = 100


class Card:
    def __init__(self):
        """Initialize attributes to describe a card_deck."""
        self.card_number = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.card_suit = ["♦️", "♥️", "♣️", "♠️"]
        self.card_deck = [number + suit for number in self.card_number for suit in self.card_suit]

    def shuffled_card(self):
        """Return the shuffled deck of cards.

        :postcondition: the cards should have four suits - hearts, diamonds, clubs, and spades
        :postcondition: the cards should have 13 different type of alphanumeric letters
        :return: a list representing shuffled card_deck
        """
        random.shuffle(self.card_deck)
        return self.card_deck

    def __str__(self):
        return self.card_deck

    def __repr__(self):
        return f"Card({self.card_deck})"


class Player:
    def __init__(self):
        """Initialize attributes to describe a player."""
        self.card = Card()
        self.dealer = Dealer()
        self.player_account = INIT_MONEY
        self.player_card = []
        self.hit_the_card = True

    def get_bet(self):
        """Get an user input regarding how much of bet the player would like to play.

        :postcondition: get the user choice of the bet
        :raise ValueError: if the user doesn't input any number
        :return: an integer representing the bet
        """
        while True:
            print(f"You have ${self.player_account} in your account.")
            print("How much do you want to bet?")
            for index, value in zip(itertools.count(1), range(MINIMUM_BET, self.player_account + 1, 10)):
                print(f"({index}) {value}", end='  ')
            try:
                input_index = input("\nEnter the number: ")
                input_value = MINIMUM_BET + (int(input_index)-1) * 10
                self.player_account -= input_value
                return input_value
            except ValueError:
                print("Please select the number.")

    def hit_init(self, card_list: list) -> list:
        """Hit the cards for a player when the game starts.

        :param card_list: a list
        :precondition: card_list must be a list representing remaining cards on the table
        :postcondition: append two cards to the player's card list
        :return: the revised card_list

        >>> player = Player()
        >>> card_deck = ['2♠️', '2♣️', '8♦️', '10♥️']
        >>> player.hit_init(card_deck)
        Player: ['10♥️', '8♦️'] | Sum: 18
        ['2♠️', '2♣️']
        >>> player.player_card
        ['10♥️', '8♦️']
        """
        self.player_card.append(card_list.pop())
        self.player_card.append(card_list.pop())

        print(f"Player: {self.player_card} | Sum: {self.get_sum()}")
        return card_list

    def hit_card(self, card_list: list) -> int:
        """Hit the cards for a player in the middle of the game round.

        :param card_list: a list
        :precondition: card_list must be a list representing remaining cards on the table
        :postcondition: the process continues until the user input "Stop" or the sum of the player's card reaches more than 21
        :postcondition: append cards to the player's card list
        :return: the sum of the player's card
        """
        while self.hit_the_card:
            action = get_player_action()
            if action == "Hit":
                self.player_card.append(card_list.pop())
                if self.get_sum() >= BLACK_JACK:  # if card sum exceeds 21, stop hitting
                    self.hit_the_card = False

            else:
                self.hit_the_card = False

            print(f"Player: {self.player_card} | Sum: {self.get_sum()}")
        return self.get_sum()

    def get_sum(self):
        """Calculate the sum of the cards the player has.

        :postcondition: invoke card_sum function to calculate
        :return: an integer

        >>> player = Player()
        >>> player.player_card = ['2♠️', '2♣️', '8♦️']
        >>> player.get_sum()
        12
        """
        return card_sum(self.player_card)

    def score_board(self):
        """Initiate the score board of the player.

        :return: a dictionary representing the score board

        >>> player = Player()
        >>> player.player_account = 100
        >>> player.score_board()
        {'Win': 0, 'Lose': 0, 'Draw': 0, 'Money': 100}
        """
        return {"Win": 0, "Lose": 0, "Draw": 0, "Money": self.player_account}

    def get_score(self, scoreboard: dict, result: str, bet: int):
        """Calculate the score and modify the score board.

        :param scoreboard: a dictionary
        :param result: a string
        :param bet: an integer
        :precondition: scoreboard must be a dictionary representing player's scoreboard
        :precondition: result must be a string either one of ["Win", "Lose", "Draw"]
        :precondition: bet must be a positive integer representing the player's bet
        :postcondition: modify the scoreboard according to the result and print the result out
        :return: no return

        >>> player = Player()
        >>> player.get_score(player.score_board(), "Win", 10)
        Player Win!
        {'Win': 1, 'Lose': 0, 'Draw': 0, 'Money': 100}
        <BLANKLINE>
        """
        if result == "Win":
            scoreboard["Win"] += 1
            self.player_account += bet
            print("Player Win!")
        elif result == "Lose":
            scoreboard["Lose"] += 1
            print(self.player_account)
            print("Player Lose!")
        else:
            scoreboard["Draw"] += 1
            self.player_account += bet
            print("Draw!")
        print(scoreboard, "\n")

    def __str__(self):
        """Return a string that represents the Player object in the format.

        :return: a string

        >>> player = Player()
        >>> player.player_card = ['9♦️', '5♣️']
        >>> print(player)
        Player's Card Deck: ['9♦️', '5♣️']
        Sum: 14
        """
        return f"Player's Card Deck: {self.player_card}\nSum: {self.get_sum()}"

    def __repr__(self):
        """Return a string that represents the Player object in the format.

        :return: a string

        >>> player = Player()
        >>> player.player_card = ['9♦️', '5♣️']
        >>> player.player_account = 20
        >>> print(repr(player))
        Player(['9♦️', '5♣️'], 20)
        """
        return f"Player({self.player_card}, {self.player_account})"


class Dealer:
    def __init__(self):
        """Initialize attributes to describe a Dealer."""
        self.card = Card()
        self.dealer_card = []
        self.hit_the_card = True

    def hit_init(self, card_list: list) -> list:
        """Hit the cards for a dealer when the game starts.

        :param card_list: a list
        :precondition: card_list must be a list representing remaining cards on the table
        :postcondition: append two cards to the dealer's card list
        :return: the revised card_list

        >>> dealer = Dealer()
        >>> card_deck = ['2♠️', '2♣️', '8♦️', '10♥️']
        >>> dealer.hit_init(card_deck)
        Dealer: ['10♥️', '8♦️'] | Sum: 18
        ['2♠️', '2♣️']
        >>> dealer.dealer_card
        ['10♥️', '8♦️']
        """
        try:
            self.dealer_card.append(card_list.pop())
            self.dealer_card.append(card_list.pop())

            print(f"Dealer: {self.dealer_card} | Sum: {self.get_sum()}")
            return card_list
        except StopIteration:
            print("EmptyDeckError: Game is over. There is no more card available.")

    def hit_card(self, card_list: list) -> int:
        """Hit the cards for a player in the middle of the game round.

        :param card_list: a list
        :precondition: card_list must be a list representing remaining cards on the table
        :postcondition: the process continues untie the sum of the dealer's card reaches more than 14
        :postcondition: append cards to the dealer's card list
        :return: the sum of the dealer's card

        >>> dealer = Dealer()
        >>> card_deck = ['2♠️', '2♣️', '8♦️', '10♥️']
        >>> print(dealer.hit_card(card_deck))
        <BLANKLINE>
        Dealer: ['10♥️'] | Sum: 10
        <BLANKLINE>
        Dealer: ['10♥️', '8♦️'] | Sum: 18
        18
        """
        while self.hit_the_card:
            self.dealer_card.append(card_list.pop())
            if self.get_sum() > DEALER_LIMIT:  # if card sum exceeds 21, stop hitting
                self.hit_the_card = False
            print(f"\nDealer: {self.dealer_card} | Sum: {self.get_sum()}")
        return self.get_sum()

    def get_sum(self):
        """Calculate the sum of the cards the player has.

        :postcondition: invoke card_sum function to calculate
        :return: an integer

        >>> dealer = Dealer()
        >>> dealer.dealer_card = ['2♠️', '2♣️', '8♦️']
        >>> dealer.get_sum()
        12
        """
        return card_sum(self.dealer_card)

    def __str__(self):
        """Return a string that represents the Dealer object in the format.

        :return: a string

        >>> dealer = Dealer()
        >>> dealer.dealer_card = ['9♦️', '5♣️']
        >>> print(dealer)
        Dealer's Card Deck: ['9♦️', '5♣️']
        """
        return f"Dealer's Card Deck: {self.dealer_card}"

    def __repr__(self):
        """Return a string that represents the Player object in the format.

        :return: a string

        >>> dealer = Dealer()
        >>> dealer.dealer_card = ['9♦️', '5♣️']
        >>> print(repr(dealer))
        Dealer(['9♦️', '5♣️'])
        """
        return f"Dealer({self.dealer_card})"


def bet_round(player_sum: int, dealer_sum: int):
    """Determine if the player wins the round by comparing the sum of both parties' cards and money the player has.

    :param player_sum: an integer
    :param dealer_sum: an integer
    :precondition: player_sum and dealer_sum must be positive integers
    :postcondition: if dealer_card < player_card <= 21, return 'Win'
    :postcondition: if dealer_card > 21, return 'Win'
    :postcondition: if player_card < dealer_card <= 21, return 'Lose'
    :postcondition: if player_card > 21, return 'Lose'
    :postcondition: if player_card = dealer_card, return 'Draw'
    :return: a string ('Win' or 'Lose' or 'Draw')

    >>> bet_round(13, 15)
    'Lose'

    >>> bet_round(21, 18)
    'Win'

    >>> bet_round(17, 17)
    'Draw'
    """
    # WIN
    if dealer_sum > BLACK_JACK or dealer_sum < player_sum <= BLACK_JACK:
        return "Win"

    # LOSE
    elif player_sum > BLACK_JACK or player_sum < dealer_sum <= BLACK_JACK:
        return "Lose"

    # DRAW
    elif player_sum == dealer_sum and player_sum <= BLACK_JACK and dealer_sum <= BLACK_JACK:
        return "Draw"


def card_sum(card_list: list) -> int:
    """Calculate the sum of the given card_list.

    :param card_list: a list
    :precondition: card_list must be a list with strings representing cards
    :postcondition: cards containing J, Q, K are worth 10
    :postcondition: card containing A is worth 1 or 11, depending on the context
    :postcondition: return the sum of the card_list which has converted elements
    :return: an integer

    >>> card_sum(['2♠️', '2♣️', '8♦️', '10♥️'])
    22

    >>> card_sum(['A♠️', '8♦️', '10♥️'])
    19
    """
    result = 0
    is_a = 0

    for i in range(len(card_list)):
        if card_list[i][0] in ['J', 'Q', 'K']:
            result += COURT_CARD
        elif card_list[i][0] == "A":
            result += 1
            is_a += 1
        else:
            if card_list[i][0] == '1':
                result += TEN_CARD
            else:
                result += int(card_list[i][0])
    return a_value(result, is_a)


def a_value(total, number):
    """Determine the value of "A" card depending on the total.

    :param total: an integer
    :param number: an integer
    :precondition: total and number must be positive integers
    :precondition: total represents the sum of the card_list
    :precondition: number represents the number of A cards in the list
    :postcondition: if the total is less than 11 and there was A in the list, add 10 to the total
    :return: an integer

    >>> a_value(11, 0)
    11

    >>> a_value(10, 2)
    20

    >>> a_value(15, 1)
    15
    """
    if number != 0:
        for _ in range(number):
            if total <= 11:
                total += A_VALUE
        return a_value(total, number-1)
    else:
        return total


def get_player_action():
    """Get player's input.

    :postcondition: return "Hit" or "Stand" according to the user's input
    :raise ValueError: if the user didn't input number
    :return: a string
    """
    try:
        action = input("\n(1) Hit (2) Stand\n")
        for index, value in enumerate(["Hit", "Stand"], 1):
            if int(action) == index:
                return value
    except ValueError:
        print("Please enter the number.")


def blackjack():
    """Play Blackjack card game."""
    player, dealer, card = Player(), Dealer(), Card()
    enough_money, enough_card = True, True

    # Get the randomly shuffled card_deck when the very first game begins
    card_deck = card.shuffled_card()
    scoreboard = player.score_board()

    # Recurse the rounds until out of card or money
    while enough_money and enough_card:
        # print out the info, Assign player's bet amount
        bet_money = player.get_bet()  # bet amount set.
        print(f"You bet ${bet_money}, and now you have ${player.player_account} remain.")

        dealer.dealer_card, player.player_card = [], []
        # Start Round
        try:
            # Hit the first two cards for each
            dealer.hit_init(card_deck)  # Dealer gets two cards, and print the sum out
            player.hit_init(card_deck)  # Player gets two cards, and print the sum out

            # Dealer hits the cards until the sum exceeds 14
            dealer.hit_card(card_deck)
            dealer_sum = dealer.hit_card(card_deck)

            # Player hits the cards until he / she wants or get BUST
            player.hit_card(card_deck)
            player_sum = player.hit_card(card_deck)

            # Check the result of the round
            # Deal with result, and print the result
            result = bet_round(player_sum, dealer_sum)
            player.get_score(scoreboard, result, bet_money)

        except IndexError:
            print("EmptyDeckError: Game is over. There is no more card available.")
            enough_card = False

        else:
            if player.player_account < MINIMUM_BET:
                print("Sorry, you don't have enough money to bet.")
                enough_money = False


def main():
    doctest.testmod(verbose=True)
    blackjack()


if __name__ == "__main__":
    main()
