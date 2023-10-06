import random
from service.card import Card

class Deck:
    """
    This class represents a deck of cards.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["HEART", "DIAMOND", "CLUB", "SPADE"]:
            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
