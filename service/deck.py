import random
from service.card import Card

class Deck:
    """
    A class representing a deck of playing cards.
    The `Deck` class has an attribute `cards` that is a list of `Card`
    objects.
    It has three methods: `build`, `shuffle`, and `draw`.
    Attributes:
        cards (List[Card]): A list of `Card` objects representing the deck of
        cards.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Build the deck of cards by appending a `Card` object for each
        combination of suit and value to the `cards` list.
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
        Remove and return the last `Card` object from the `cards` list.
        """
        return self.cards.pop()
