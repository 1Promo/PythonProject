import pytest
from unittest.mock import patch, MagicMock
from external_api import convert_to_rub


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {"rates": {"RUB": 90.5}, "success": True}
    mock.ok = True
    return mock


def test_convert_to_rub_rub():
    transaction = {"amount": "100.0", "currency": "RUB"}
    assert convert_to_rub(transaction) == 100.0


@patch("external_api.requests.get")
def test_convert_to_rub_usd(mock_get, mock_response):
    mock_get.return_value = mock_response
    transaction = {"amount": "10.0", "currency": "USD"}
    assert convert_to_rub(transaction) == 905.0


@patch("external_api.requests.get")
def test_convert_to_rub_eur(mock_get, mock_response):
    mock_get.return_value = mock_response
    transaction = {"amount": "5.0", "currency": "EUR"}
    assert convert_to_rub(transaction) == 452.5


def test_convert_to_rub_unsupported_currency():
    transaction = {"amount": "100.0", "currency": "GBP"}
    with pytest.raises(ValueError, match="Unsupported currency"):
        convert_to_rub(transaction)


@patch.dict("external_api.os.environ", {}, clear=True)
def test_convert_to_rub_no_api_key():
    transaction = {"amount": "10.0", "currency": "USD"}
    with pytest.raises(ValueError, match="API key not configured"):
        convert_to_rub(transaction)


@patch("external_api.requests.get")
def test_convert_to_rub_api_failure(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.text = "API error"
    mock_get.return_value = mock_response

    transaction = {"amount": "10.0", "currency": "USD"}
    with pytest.raises(ValueError, match="API request failed"):
        convert_to_rub(transaction)
