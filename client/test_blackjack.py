import pytest
from flask_testing import TestCase
from app import app, deck, player_hand, dealer_hand

class FlaskAppTest(TestCase):
    """
    A class for testing the Flask application.
    """

    def create_app(self):
        """
        Create and configure the Flask app for testing.
        Returns:
            Flask app: The configured Flask app.
        """
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """
        Set up the test environment by initializing the deck and hands.
        """
        # Executed before every test
        self.deck = deck
        self.deck.shuffle()
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def tearDown(self):
        """
        Perform any necessary cleanup after each test.
        """
        # Executed after every test
        pass

    def test_start_game(self):
        """
        Test the /start endpoint of the application.
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
        Test the /hit endpoint of the application.
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
        Test the /stand endpoint of the application.
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
