import pytest
from get_weather import get_weather

def test_get_weather(mocker):
    mock_get = mocker.patch("get_weather.requests.get")

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}

    result = get_weather("Dubai")

    assert result == {"temperature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")