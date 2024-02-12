import pytest
from flask_testing import TestCase
from app import app, deck, player_hand, dealer_hand

class FlaskAppTest(TestCase):
    """Test suite for the card game Flask app."""

    def create_app(self):
        """Create and configure the Flask app for testing."""
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Set up test data for each test."""
        # Executed before every test
        self.deck = deck
        self.deck.shuffle()
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def tearDown(self):
        """Clean up test data after each test."""
        # Executed after every test
        pass

    def test_start_game(self):
        """Test that the game can be started and the initial hands are
dealt."""
        response = self.client.get('/start')
        json_response = response.get_json()
        self.assert200(response)
        assert 'player' in json_response
        assert 'dealer' in json_response
        assert len(json_response['player']) == 2
        assert len(json_response['dealer']) == 2

    def test_hit(self):
        """Test that a player can hit and receive a card."""
        # Start a game first
        self.client.get('/start')
        response = self.client.get('/hit')
        json_response = response.get_json()
        self.assert200(response)
        assert 'player' in json_response
        assert len(json_response['player']) >= 3  # Because we've hit once

    def test_stand(self):
        """Test that a player can stand and the game continues."""
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
