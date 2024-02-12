import json
from typing import Optional

class User:
    """
    Represents a user in a simple casino game.
    Attributes:
        name (str): The user's name.
        chips (int): The user's current chip count.
        highest_amount (int): The user's highest chip count ever reached.
    """

    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.highest_amount = chips

    def bet(self, amount: int):
        """
        Allows the user to place a bet, deducting the bet amount from
        their chips if they have enough.
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
        Increases the user's chips by the given amount and updates
        their highest_amount if the new chip count is higher.
        Args:
            amount (int): The amount to add to the user's chips.
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
        Class method to load a user's data from the JSON file,
        returning a new User instance if the user exists or None if not.
        Args:
            name (str): The name of the user to load.
        Returns:
            Optional[User]: A new User instance if the user exists, or None if not.
        """
        with open("./data/users.json", "r") as file:
            users = json.load(file)
            if name in users:
                user_data = users[name]
                user = User(name, user_data["chips"])
                user.highest_amount = user_data["highest_amount"]
                return user
        return None
