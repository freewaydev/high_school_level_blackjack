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
    Join the game by providing a user name.
    This route is a POST request that allows a user to join the game by providing their
    name. If the provided name does not exist in the users.json file, a new User instance is
    created and saved to the file.
    :returns: A JSON response containing the user's name, chips amount, and highest amount.
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
    Start the game by dealing two cards to the player and two cards to the dealer.
    This route is a GET request that starts the game by dealing two cards to the player and
    two cards to the dealer from the shuffled deck.
    :returns: A JSON response containing the player's hand and the dealer's hand, with the
    first card of the dealer's hand hidden.
    """
    global player_hand, dealer_hand, deck

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    return jsonify(player=display_hand(player_hand), dealer=display_hand(dealer_hand, hide_first=True))

@app.route('/hit', methods=['GET'])
def hit():
    """
    Draw an additional card for the player.
    This route is a GET request that allows the player to draw an additional card from the
    deck. If the player's hand exceeds 21, the player busts and loses the game.
    :returns: A JSON response containing the player's hand. If the player busts, the
    response also includes a status message.
    """
    global player_hand
    player_hand.append(deck.draw())
    if calculate_total(player_hand) > 21:
        return jsonify(status="Player busted!", player=display_hand(player_hand))
    return jsonify(player=display_hand(player_hand))

@app.route('/stand', methods=['GET'])
def stand():
    """
    Executes the logic for the '/stand' route.
    Calculates the total value of the dealer's hand and the player's hand, and determines
    the outcome of the game (Dealer wins, Player wins, or Tie) based on the values.
    :returns: JSON response with the outcome of the game and the dealer's hand.
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
    Calculates the total value of a hand.
    :arg hand: The hand for which the total value needs to be calculated.
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
    Displays the cards in a hand.
    :arg hand: The hand to be displayed.
    :kwarg hide_first: A boolean indicating whether the first card should be hidden.
    Defaults to False.
    :returns: The list of cards in the hand.
    """
    if hide_first:
        return ["hidden"] + [f"{card.value} of {card.suit}" for card in hand[1:]]
    return [f"{card.value} of {card.suit}" for card in hand]

if __name__ == '__main__':
    app.run(debug=True)
