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
    Join the game by creating a new user or loading an existing user.

    This route handles a POST request to join the game. It expects a
    JSON payload
    with a 'name' field. If the user with the specified name already exists, their
    information will be loaded. Otherwise, a new user will be created with the given
    name. The user's name, chips, and highest_amount will be returned in the response.

    Returns:
        JSON: The user's name, chips, and highest_amount.
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
    Start the game by dealing the initial hands.

    This route handles a GET request to start the game. It deals two
    cards to the player and two cards to the dealer. The player's hand and the dealer's
    hand (with the first card hidden) will be returned in the response.

    Returns:
        JSON: The player's hand and the dealer's hand.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Draw a new card for the player.

    This route handles a GET request to draw a new card for the player.
    It draws a card
    from the deck and adds it to the player's hand. If the player's total exceeds 21,
    the response will indicate that the player busted. Otherwise, the player's hand
    will be returned in the response.

    Returns:
        JSON: The player's hand, and if the player busted, a status message.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))


@app.route('/stand', methods=['GET'])
def stand():
    """
    Route handler for the '/stand' endpoint.

    This function is triggered by a GET request. It continues to draw
    cards for the dealer until their total value reaches 17 or higher.
    Then, it compares the dealer's total with the player's total and
    returns a JSON response with the appropriate status message and the dealer's hand.
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
    Calculate the total value of a hand.

    This function sums the values of the cards in the hand. If the
    total exceeds 21 and there are aces in the hand, it adjusts the total by
    subtracting 10 for each ace until the total is less than or equal to 21.

    Args:
        hand (list): A list of Card objects representing the hand.

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
    Return a list of strings representing the cards in a hand.

    This function takes a list of Card objects representing a hand and
    returns a list of strings describing the cards. If 'hide_first' is
    True, the first card is replaced with the string 'hidden'.

    Args:
        hand (list): A list of Card objects representing the hand.
        hide_first (bool): Whether to hide the first card or not.

    Returns:
        list: A list of strings describing the cards in the hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
