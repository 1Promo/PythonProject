import pytest
import requests
from unittest.mock import Mock, patch
from external_api import _get_exchange_rate, convert_to_rub


# Тесты для функции _get_exchange_rate
@patch('external_api.requests.get')
def test_successful_usd_conversion(mock_get):
    """Успешная конвертация USD в RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 92.5}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = _get_exchange_rate("USD", 100.0)

    assert result == 92.5
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        params={"to": "RUB", "from": "USD", "amount": 100.0},
        headers={"apikey": None},
        timeout=10
    )


@patch('external_api.requests.get')
def test_successful_eur_conversion(mock_get):
    """Успешная конвертация EUR в RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 101.3}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = _get_exchange_rate("EUR", 50.0)

    assert result == 101.3


@patch('external_api.os.getenv', return_value=None)
def test_missing_api_key(mock_getenv):
    """Ошибка при отсутствии API ключа"""
    with pytest.raises(ValueError, match="API ключ не настроен"):
        _get_exchange_rate("USD", 100.0)

@patch('external_api.requests.get')
def test_api_connection_error(mock_get):
    """Ошибка соединения с API"""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

    with pytest.raises(ValueError, match="Ошибка соединения с API"):
        _get_exchange_rate("USD", 100.0)


# Тесты для функции convert_to_rub
def test_rub_transaction():
    """Транзакция уже в RUB - возвращается исходная сумма"""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"code": "RUB"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 1500.50


@patch('external_api._get_exchange_rate')
def test_usd_transaction(mock_get_rate):
    """Конвертация USD в RUB"""
    mock_get_rate.return_value = 9200.0

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 9200.0
    mock_get_rate.assert_called_once_with("USD", 100.0)


@patch('external_api._get_exchange_rate')
def test_eur_transaction(mock_get_rate):
    """Конвертация EUR в RUB"""
    mock_get_rate.return_value = 5050.0

    transaction = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"code": "EUR"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 5050.0
    mock_get_rate.assert_called_once_with("EUR", 50.0)


    with pytest.raises(ValueError, match="Ошибка конвертации суммы"):
        convert_to_rub(transaction)


@patch('external_api._get_exchange_rate')
def test_api_error_propagation(mock_get_rate):
    """Ошибка из _get_exchange_rate пробрасывается правильно"""
    mock_get_rate.side_effect = ValueError("API error message")

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="API error message"):
        convert_to_rub(transaction)
