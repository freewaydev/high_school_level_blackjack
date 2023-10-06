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
    Join the game by providing a name.

    This route allows a user to join the game by providing their name.
    If the user is new, a new User object is created and saved. If the
    user already exists, their information is loaded from the 'users.json' file.

    Returns:
        dict: A dictionary containing the user's name, chips, and highest amount.
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
    Start the game by initializing the player's and dealer's hands.

    This route starts the game by initializing the player's and
    dealer's hands with two cards each. The hands are drawn from a shuffled deck.

    Returns:
        dict: A dictionary containing the player's and dealer's hands.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Draw an additional card for the player.

    This route allows the player to draw an additional card. If the
    player's total exceeds 21, they bust and lose the game.

    Returns:
        dict: A dictionary containing the player's hand and the game status.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))


@app.route('/stand', methods=['GET'])
def stand():
    """
    Handle GET requests to the '/stand' endpoint.

    This function updates the dealer's hand by drawing cards from the
    deck until the total value of the hand is 17 or higher. It then compares the total
    value of the dealer's hand with the player's hand and returns a JSON response with
    the game status and the dealer's hand.
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
    total = sum(card.get_value() for card in hand)
    num_aces = sum(1 for card in hand if card.value == 'A')
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total

def display_hand(hand, hide_first=False):
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
