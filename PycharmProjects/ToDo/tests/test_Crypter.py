import pytest
from Crytpter import *

@pytest.mark.parametrize("text, expected_hash", [
    ("aze", "9adfb0a6d03beb7141d8ec2708d6d9fef9259d12cd230d50f70fb221ae6cabd5"),
    ("pomme", "9169bf3e501fea19614cacd6d646b50b63aa822bc2360a4db06aee4cd504cb4f"),
    ("bonjour", "2cb4b1431b84ec15d35ed83bb927e27e8967d75f4bcd9cc4b25c8d879ae23e18"),
    ("8BXz9Lw", "febbe6b7563378a35d12527f3afddd2d42975f60b949ddeb857b6d05a85fc3a1"),
    ("Kr!t?K4", "d7c8287985d406b3ba413d4fa790086e3b7b36485603a56f4fb4b22e7e11ef2e"),
    ("M3czE&N?4bSi", "eea1d6adae8a818acd916403c3cfe8776f3e1e2385a9b7518eeda8268f5640fc"),
])

def test_hash_(text, expected_hash):
    assert hash_(text) == expected_hash