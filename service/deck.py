import random
from service.card import Card

class Deck:
    """
    This class represents a deck of playing cards.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Build a full deck of 52 cards by iterating over all possible
        suits and values and appending a new Card object to the cards list for
        each combination.
        """
        for suit in ["HEART", "DIAMOND", "CLUB", "SPADE"]:
            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Shuffle the deck of cards using the random.shuffle function.
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        Draw and return the last card from the deck by popping it from
        the cards list.
        """
        return self.cards.pop()
