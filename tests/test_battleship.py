import pytest

from ..battleship import Battleship


# Tests for methods used for game setup.
def test_ship_size():
    """Test for ship_size method."""
    game = Battleship()
    result = game.ship_size()

    assert result in [1, 2, 3]


# Tests for methods used during the game.
def test_check_ship_location():
    """Test for check_ship_location method."""
    battleships = [
        [
            [0, 1, 3],
            ],
    ]
    x = 1
    y = 3
    game = Battleship()
    result = game.check_ship_location(battleships, x, y)

    assert result is True

# Tests for statistics methods
