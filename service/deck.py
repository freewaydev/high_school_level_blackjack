import random
from service.card import Card

class Deck:
    """
    Represents a deck of playing cards.
    Attributes:
        cards (list): A list of Card instances.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Builds the deck by creating Card instances for each suit and
        value combination.
        """
        for suit in ["HEART", "DIAMOND", "CLUB", "SPADE"]:
            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Shuffles the deck using the random.shuffle function.
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        Draws and returns a card from the deck by popping the last item
        in the cards list.
        Returns:
            Card: The drawn card.
        """
        return self.cards.pop()
