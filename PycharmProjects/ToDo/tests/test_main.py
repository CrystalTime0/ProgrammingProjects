import os.path
import pytest
import json

from orca.debug import println

from config import *
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
@pytest.fixture
def data_path():
    return DATA_PATH

def test_save_user_data(all_user_data):
    save_user_data(all_user_data)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        generated_all_users_data = json.load(f)

    assert all_user_data == generated_all_users_data

def test_load_user_data(data_path,all_user_data):
    assert os.path.exists(data_path)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        decoder = json.JSONDecoder()
        data_str = f.read()
        loaded_data, i = decoder.raw_decode(data_str)

    assert loaded_data == all_user_data
