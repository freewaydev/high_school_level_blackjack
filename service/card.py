class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        """Return the value of the card, treating face cards as 10 and aces as
11."""
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
