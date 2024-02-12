class Card:
    """
    A class representing a playing card with a suit and value.
    This class initializes a playing card with a specified suit and value,
    and provides a method to get the card's value as an integer.
    Attributes:
        suit (str): The suit of the card (e.g. "hearts", "diamonds",
        "clubs", or "spades").
        value (str): The value of the card (e.g. "2", "3", ..., "10",
        "J", "Q", "K", or "A").
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        """
        Get the card's value as an integer.
        Returns:
            int: The card's value as an integer.
        """
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
