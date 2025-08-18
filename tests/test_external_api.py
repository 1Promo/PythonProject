import pytest
from unittest.mock import patch, MagicMock

import requests

from external_api import CurrencyConverter


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {'rates': {'RUB': 90.5}, 'success': True}
    mock.raise_for_status.return_value = None
    return mock


def test_convert_rub():
    """Тест конвертации RUB в RUB (должна возвращать ту же сумму)"""
    converter = CurrencyConverter()
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {'code': 'RUB'}
        }
    }
    assert converter.convert_to_rub(transaction) == 100.0


@patch('requests.get')
def test_convert_usd(mock_get, mock_response):
    """Тест конвертации USD в RUB"""
    mock_get.return_value = mock_response
    converter = CurrencyConverter()
    transaction = {
        'operationAmount': {
            'amount': '10.0',
            'currency': {'code': 'USD'}
        }
    }
    assert converter.convert_to_rub(transaction) == 905.0


def test_invalid_currency():
    """Тест на неподдерживаемую валюту"""
    converter = CurrencyConverter()
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {'code': 'GBP'}
        }
    }
    with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
        converter.convert_to_rub(transaction)


def test_invalid_structure():
    """Тест на неверную структуру транзакции"""
    converter = CurrencyConverter()
    with pytest.raises(ValueError, match="Неверная структура транзакции"):
        converter.convert_to_rub({'invalid': 'data'})


@patch('requests.get')
def test_api_failure(mock_get):
    """Тест ошибки API"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.RequestException("API error")
    mock_get.return_value = mock_response

    converter = CurrencyConverter()
    transaction = {
        'operationAmount': {
            'amount': '10.0',
            'currency': {'code': 'USD'}
        }
    }
    with pytest.raises(ValueError, match="Ошибка API"):
        converter.convert_to_rub(transaction)
