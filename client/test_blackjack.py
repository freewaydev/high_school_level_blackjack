import pytest
from flask_testing import TestCase
from app import app, deck, player_hand, dealer_hand

class FlaskAppTest(TestCase):
    """
    A class for testing the functionality of a Flask application.
    """

    def create_app(self):
        """
        Creates and configures the Flask app for testing.
        Returns:
            Flask app
        """
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """
        Executed before every test. Initializes the deck and hands for
        the player and dealer.
        """
        # Executed before every test
        self.deck = deck
        self.deck.shuffle()
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def tearDown(self):
        """
        Executed after every test. Performs any necessary cleanup.
        """
        # Executed after every test
        pass

    def test_start_game(self):
        """
        Tests the /start route. Checks that the response is successful
        and contains the expected JSON data.
        """
        response = self.client.get('/start')
        json_response = response.get_json()
        self.assert200(response)
        assert 'player' in json_response
        assert 'dealer' in json_response
        assert len(json_response['player']) == 2
        assert len(json_response['dealer']) == 2

    def test_hit(self):
        """
        Tests the /hit route. Checks that the response is successful
        and that the player's hand has at least three cards.
        """
        # Start a game first
        self.client.get('/start')
        response = self.client.get('/hit')
        json_response = response.get_json()
        self.assert200(response)
        assert 'player' in json_response
        assert len(json_response['player']) >= 3  # Because we've hit once

    def test_stand(self):
        """
        Tests the /stand route. Checks that the response is successful
        and contains the expected JSON data.
        """
        # Start a game first
        self.client.get('/start')
        response = self.client.get('/stand')
        json_response = response.get_json()
        self.assert200(response)
        assert 'dealer' in json_response
        assert 'status' in json_response

# More tests can be added similarly

if __name__ == '__main__':
    pytest.main()
