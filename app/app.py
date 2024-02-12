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
    """
    Join the Blackjack game by providing a name.
    This route accepts a POST request with a JSON payload containing a
    'name' field.
    If the user does not exist, a new user is created and saved. The
    user's name, chips, and highest_amount are returned in the response.
    Returns:
        A JSON response containing the user's name, chips, and highest_amount.
    """
    name = request.json.get('name')
    user = User.load(name)
    if not user:
        user = User(name)
        user.save()
    return jsonify(name=user.name, chips=user.chips, highest_amount=user.highest_amount)


@app.route('/start', methods=['GET'])
def start_game():
    """
    Start the Blackjack game by dealing initial cards.
    This route accepts a GET request and deals two cards to both the
    player and the dealer.
    The player's and dealer's hands are returned in the response, with
    the dealer's first card hidden.
    Returns:
        A JSON response containing the player's and dealer's hands.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Draw an additional card for the player.
    This route accepts a GET request and deals an additional card to
    the player.
    If the player's total exceeds 21, the response indicates that the
    player has busted.
    Otherwise, the updated player's hand is returned in the response.
    Returns:
        A JSON response containing the player's updated hand.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))

@app.route('/stand', methods=['GET'])
def stand():
    """
    Handle the dealer's actions when the player decides to stand.
    This function calculates the total value of the dealer's hand,
    checking if it goes over 17, 21, or if the player has a higher total.
    Returns:
        jsonify(status, dealer): A JSON response containing the game status
        and the dealer's hand.
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
    Calculate the total value of a given hand.
    This function considers the possibility of Aces being either 1 or 11.
    Args:
        hand (list): A list of cards representing the hand.
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
    Format a given hand to be displayed to the user.
    Args:
        hand (list): A list of cards representing the hand.
        hide_first (bool): Whether to hide the first card or not.
        Defaults to False.
    Returns:
        list: A list of strings representing the formatted hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
