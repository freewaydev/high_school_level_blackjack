from flask import Flask, jsonify, request
from service.deck import Deck
from service.user import User
import os
import json

app = Flask(__name__)

# Ensure data folder exists
if not os.path.exists('./data'):
    os.makedirs('./data')

# Ensure users.json exists
if not os.path.exists('./data/users.json'):
    with open('./data/users.json', 'w') as file:
        json.dump({}, file)

deck = Deck()
deck.shuffle()

player_hand = []
dealer_hand = []


@app.route('/join', methods=['POST'])
def join_game():
    """Join the game and create a new user if one does not exist."""
    name = request.json.get('name')
    user = User.load(name)
    if not user:
        user = User(name)
        user.save()
    return jsonify(name=user.name, chips=user.chips, highest_amount=user.highest_amount)


@app.route('/start', methods=['GET'])
def start_game():
    """Start the game by dealing two cards to the player and dealer."""
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """Deal another card to the player."""
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))

@app.route('/stand', methods=['GET'])
def stand():
    """
    Simulate the dealer's turn in a blackjack game and return the game
    status and dealer's hand.
    This function handles the /stand endpoint of the API and calculates
    the total of the dealer's hand.
    If the total is less than 17, the dealer will keep drawing cards
    until the total is 17 or more.
    The function then checks if the dealer has busted (total greater
    than 21), and returns the game status and the dealer's hand accordingly.
    Returns:
        A JSON response containing the game status and the dealer's hand.
    """
    global dealer_hand
    while calculate_total(dealer_hand) < 17:
        dealer_hand.append(deck.draw())
    if calculate_total(dealer_hand) > 21:
        return jsonify(status="Dealer busted!", dealer=display_hand(dealer_hand))
    elif calculate_total(dealer_hand) > calculate_total(player_hand):
        return jsonify(status="Dealer wins!", dealer=display_hand(dealer_hand))
    elif calculate_total(dealer_hand) < calculate_total(player_hand):
        return jsonify(status="Player wins!", dealer=display_hand(dealer_hand))
    else:
        return jsonify(status="It's a tie!", dealer=display_hand(dealer_hand))

def calculate_total(hand):
    """
    Calculate the total value of a hand in a blackjack game.
    This function calculates the total value of a hand by summing the
    values of all cards in the hand.
    It also takes into account the presence of aces (value 1 or 11) to
    ensure the total is as high as possible without going over 21.
    Args:
        hand (list): A list of Card objects representing a hand.
    Returns:
        int: The total value of the hand.
    """
    total = sum(card.get_value() for card in hand)
    num_aces = sum(1 for card in hand if card.value == 'A')
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total

def display_hand(hand, hide_first=False):
    """
    Display a hand in a blackjack game, optionally hiding the first card.
    This function returns a string representation of a hand. If
    `hide_first` is True, the first card will be
    represented as "hidden". Otherwise, all cards will be displayed normally.
    Args:
        hand (list): A list of Card objects representing a hand.
        hide_first (bool, optional): Whether to hide the first card in the
            hand. Defaults to False.
    Returns:
        list: A list of strings representing the hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
