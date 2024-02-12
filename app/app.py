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
    Join a game with a specified name. If the user does not exist, a
    new user is created.
    Returns:
        A JSON object containing the user's name, chips, and highest
        amount won.
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
    Start a new game by initializing player and dealer hands.
    Returns:
        A JSON object containing the player's and dealer's hands.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Draw a card for the player. If the player's total exceeds 21, the
    game is over.
    Returns:
        A JSON object containing the player's updated hand.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))

@app.route('/stand', methods=['GET'])
def stand():
    """
    Handle the game logic when a player decides to stand in a blackjack
    game.
    This function checks if the dealer's hand is less than 17 and, if
    so, draws cards until the total value of the dealer's hand is 17 or
    greater. Then, the function compares the total values of the dealer's and
    player's hands to determine the winner and returns the result as a JSON
    object.
    Returns:
        jsonify: A JSON object containing the game result.
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
    This function takes into account the possibility of Aces being
    worth either 1 or 11.
    Args:
        hand (list): A list of Card objects.
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
    Display a hand in a blackjack game.
    This function takes a list of Card objects and returns a list of
    strings representing the cards in the hand. If `hide_first` is True, the
    first card is represented as "hidden".
    Args:
        hand (list): A list of Card objects.
        hide_first (bool, optional): If True, hide the first card.
        Defaults to False.
    Returns:
        list: A list of strings representing the cards in the hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
