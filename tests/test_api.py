from unittest.mock import patch
import requests
from api_monitor import check_api


@patch("api_monitor.requests.get")
def test_api_is_healthy(mock_get):

    mock_get.return_value.status_code = 200

    result = check_api("http://fake-api")

    assert result["status_code"] == 200
    assert result["healthy"] is True


@patch("api_monitor.requests.get")
def test_api_is_unhealthy(mock_get):

    mock_get.return_value.status_code = 500

    result = check_api("http://fake-api")

    assert result["status_code"] == 500
    assert result["healthy"] is False


@patch("api_monitor.requests.get")
def test_api_connection_failure(mock_get):

    mock_get.side_effect = requests.RequestException()

    result = check_api("http://fake-api")

    assert result["status_code"] is None
    assert result["healthy"] is False

