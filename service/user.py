import json
from typing import Optional

class User:
    """
    Represents a user in a game.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current amount of chips.
        highest_amount (int): The user's highest amount of chips.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Allows the user to place a bet, deducting the bet amount from
        their chips if it's a valid bet.
        Args:
            amount (int): The amount of chips to bet.
        Returns:
            bool: True if the bet was successful, False otherwise.
        """
        if amount <= self.chips:
            self.chips -= amount
            return True
        return False

    def win(self, amount: int):
        """
        Adds the specified amount to the user's chips and updates their
        highest amount of chips if necessary.
        Args:
            amount (int): The amount of chips to add.
        """
        self.chips += amount
        if self.chips > self.highest_amount:
            self.highest_amount = self.chips

    def save(self):
        """
        Saves the user's data to a JSON file.
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
        Loads a user's data from a JSON file and returns a new User
        instance with that data.
        Args:
            name (str): The name of the user to load.
        Returns:
            Optional[User]: A new User instance with the loaded data,
            or None if the user doesn't exist in the file.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
