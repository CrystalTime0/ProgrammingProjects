import os.path

import pytest
from src.main import save_user_data

@pytest.fixture
def all_user_data():
    return {
    "Romain": {
        "password": "9adfb0a6d03beb7141d8ec2708d6d9fef9259d12cd230d50f70fb221ae6cabd5",
        "xp": 100
    },
    "Benoit": {
        "password": "qsd",
        "xp": 200
    },
    "Lucas": {
        "password": "wxc",
        "xp": 300
    }
}

def test_save_user_data(all_user_data):
    save_user_data(all_user_data)

def test_load_user_data():
    assert os.path.exists(da)