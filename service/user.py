import json
from typing import Optional

class User:
    """
    A class representing a user in a game.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current number of chips.
        highest_amount (int): The user's highest number of chips ever reached.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Place a bet with the given amount.
        Args:
            amount (int): The amount to bet.
        Returns:
            bool: True if the bet is successful, False otherwise.
        """
        if amount <= self.chips:
            self.chips -= amount
            return True
        return False

    def win(self, amount: int):
        """
        Increase the user's chips by the given amount.
        Args:
            amount (int): The amount to add to the user's chips.
        """
        self.chips += amount
        if self.chips > self.highest_amount:
            self.highest_amount = self.chips

    def save(self):
        """
        Save the user's data to a JSON file.
        """
        with open("./data/users.json", "r+") as file:
            users = json.load(file)
            users[self.name] = {
                "chips": self.chips,
                "highest_amount": self.highest_amount
            }
            file.seek(0)
            json.dump(users, file)

    @classmethod
    def load(cls, name: str) -> Optional['User']:
        """
        Load a user's data from a JSON file and return a User instance.
        Args:
            name (str): The user's name.
        Returns:
            User or None: A User instance if the user is found, None otherwise.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
