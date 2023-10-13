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
    Creates a new User instance if the name does not exist in the users.json file.
    Returns the name, chips, and highest_amount of the user.
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
    Start a new game.
    Shuffles the deck and deals two cards to the player and the dealer.
    Returns the player's hand and the dealer's hand.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Player draws an additional card.
    Adds a card to the player's hand.
    If the player's total exceeds 21, they bust and lose the game.
    Returns the player's hand.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))

@app.route('/stand', methods=['GET'])
def stand():
    """
    Handle a GET request for the '/stand' endpoint.
    This function performs the logic for the dealer's turn in a blackjack game. It
    calculates the total value of the dealer's hand and decides whether the dealer wins, the
    player wins, or it's a tie. It returns a JSON response with the game status and the dealer's
    hand.
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
    This function calculates the total value of a hand by summing the values of all the
    cards in the hand. It also adjusts the total if there are aces in the hand.
    :arg hand: The hand of cards.
    :returns: The total value of the hand.
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
    This function returns a list of strings representing the cards in a hand. If
    'hide_first' is True, the first card is hidden.
    :arg hand: The hand of cards.
    :kwarg hide_first: Whether to hide the first card. Defaults to False.
    :returns: A list of strings representing the cards in the hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
