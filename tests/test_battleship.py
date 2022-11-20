import pytest

from ..battleship import Battleship


def test_ship_size():
    """Test for ship_size method."""
    game = Battleship()
    result = game.ship_size()

    assert result in [1, 2, 3]
