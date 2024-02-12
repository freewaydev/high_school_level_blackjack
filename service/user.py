import json
from typing import Optional

class User:
    """
    Represents a user in a game with a name, chips, and highest_amount.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current chips.
        highest_amount (int): The highest amount of chips the user has ever
        had.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Place a bet with a specified amount.
        If the user has enough chips, the bet is successful, and the
        user's chips are updated accordingly.
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
        Increase the user's chips by the specified amount and update
        the highest_amount if necessary.
        Args:
            amount (int): The amount to win.
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
        Load a user's data from a JSON file and return a User object.
        Args:
            name (str): The name of the user to load.
        Returns:
            Optional[User]: The loaded user or None if the user is not found.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
