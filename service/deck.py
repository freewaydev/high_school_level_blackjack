import random
from service.card import Card

class Deck:
    """
    Represents a deck of playing cards.
    Attributes:
        cards (List[Card]): A list of Card instances representing the deck.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Generates a list of 52 Card instances representing all possible
        card combinations.
        This method iterates through all possible suits and values,
        creating and appending a new Card instance for each combination.
        """
        for suit in ["HEART", "DIAMOND", "CLUB", "SPADE"]:
            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Randomly shuffles the cards in the deck.
        This method uses the random.shuffle() function to rearrange the
        cards in the self.cards list.
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        Draws and returns a card from the deck, removing it from the
        list of cards.
        Returns:
            Card: The next card in the deck.
        """
        return self.cards.pop()
