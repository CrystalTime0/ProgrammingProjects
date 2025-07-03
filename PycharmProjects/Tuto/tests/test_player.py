import pytest

from player import *


@pytest.fixture()
def player():
    return Player()

def test_add_item(player):
    assert player.add_item("carrot") == True

def test_add_duplicate_item(player):
    player.add_item("carrot")
    with pytest.raises(ValueError):
        player.add_item("carrot")