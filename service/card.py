class Card:
    """
    A class representing a playing card with a suit and value.
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        """
        Return the value of the card as an integer.
        If the value is a jack, queen, or king, return 10. If the value
        is an ace, return 11. Otherwise, return the value as an integer.
        Returns:
            int: The value of the card as an integer.
        """
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
