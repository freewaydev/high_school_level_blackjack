import json
from typing import Optional

class User:
    """
    Represents a user in a game.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current amount of chips.
        highest_amount (int): The user's highest amount won so far.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Allows the user to place a bet of a specified amount of chips,
        as long as they have enough chips.
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
        Allows the user to win a specified amount of chips, which is
        added to their current amount.
        If the user's new chip count is higher than their highest
        amount won so far, it is updated.
        Args:
            amount (int): The amount of chips won.
        """
        self.chips += amount
        if self.chips > self.highest_amount:
            self.highest_amount = self.chips

    def save(self):
        """
        Saves the user's current chip and highest amount won data to a
        JSON file.
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
        Class method that loads a user's data from a JSON file, based
        on their name.
        Args:
            name (str): The user's name.
        Returns:
            Optional[User]: The loaded user object, or None if the user
            was not found.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
