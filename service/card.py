class Card:
    """
    Represents a playing card.
    :arg suit: The suit of the card.
    :arg value: The face value of the card.
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
