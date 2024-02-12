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
        Build a full deck of 52 Card objects and append them to the
        `cards` list.
        """
        for suit in ["HEART", "DIAMOND", "CLUB", "SPADE"]:
            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Shuffle the `cards` list using the `random.shuffle` function.
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        Remove and return the last Card object from the `cards` list.
        """
        return self.cards.pop()
