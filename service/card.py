class Card:
    """
    A class representing a playing card with a suit and value.
    This class initializes a playing card with a specified suit and value.
    It also includes a method to get the value of the card.
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        """
        Get the value of the card.
        This method returns the value of the card as an integer.
        If the value is 'J', 'Q', or 'K', it returns 10.
        If the value is 'A', it returns 11.
        Otherwise, it returns the value as an integer.
        Returns:
            int: The value of the card as an integer.
        """
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
