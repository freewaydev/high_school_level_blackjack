import json
from typing import Optional

class User:
    """
    Represents a user in a game or application.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current chip count.
        highest_amount (int): The user's highest chip count.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Allows the user to place a bet up to their current chip count.
        Args:
            amount (int): The amount to bet.
        Returns:
            bool: True if the bet was successful, False otherwise.
        """
        if amount <= self.chips:
            self.chips -= amount
            return True
        return False

    def win(self, amount: int):
        """
        Increases the user's chip count by the given amount and updates
        their highest chip count if necessary.
        Args:
            amount (int): The amount won.
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
        Loads a user's data from a JSON file and returns a User instance.
        Args:
            name (str): The name of the user to load.
        Returns:
            Optional[User]: The loaded user or None if the user does not exist.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
