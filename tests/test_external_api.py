import unittest
from unittest.mock import patch, MagicMock
from main import convert_to_rub
from external_api import _get_exchange_rate
import requests


def test_rub_transaction():
    """Тест транзакции в рублях - не должен вызывать API"""
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}

    with patch("main._get_exchange_rate") as mock_rate:
        result = convert_to_rub(transaction)

        assert result == 100.50
        assert isinstance(result, float)
        mock_rate.assert_not_called()


def test_usd_transaction_success():
    """Тест успешной конвертации USD"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    with patch("main._get_exchange_rate") as mock_rate:
        mock_rate.return_value = 7500.50
        result = convert_to_rub(transaction)

        assert result == 7500.50
        mock_rate.assert_called_once_with("USD", 100.00)


def test_eur_transaction_success():
    """Тест успешной конвертации EUR"""
    transaction = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}

    with patch("main._get_exchange_rate") as mock_rate:
        mock_rate.return_value = 4500.25
        result = convert_to_rub(transaction)

        assert result == 4500.25
        mock_rate.assert_called_once_with("EUR", 50.00)


def test_unsupported_currency():
    """Тест неподдерживаемой валюты"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}

    try:
        convert_to_rub(transaction)
        assert False, "Должно было возникнуть исключение"
    except ValueError as e:
        assert "Неподдерживаемая валюта" in str(e)


def test_missing_operation_amount():
    """Тест отсутствия поля operationAmount"""
    transaction = {"amount": "100.00"}

    try:
        convert_to_rub(transaction)
        assert False, "Должно было возникнуть исключение"
    except ValueError as e:
        assert "отсутствует поле" in str(e)


def test_missing_amount_field():
    """Тест отсутствия поля amount"""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}

    try:
        convert_to_rub(transaction)
        assert False, "Должно было возникнуть исключение"
    except ValueError as e:
        assert "отсутствует поле" in str(e)


def test_missing_currency_code():
    """Тест отсутствия поля code в currency"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"name": "US Dollar"}}}

    try:
        convert_to_rub(transaction)
        assert False, "Должно было возникнуть исключение"
    except ValueError as e:
        assert "отсутствует поле" in str(e)


def test_get_exchange_rate_success():
    """Тест успешного получения курса через API"""
    with patch("external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 75.50}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = _get_exchange_rate("USD", 100.00)
        assert result == 75.50


def test_get_exchange_rate_api_error():
    """Тест ошибки API"""
    with patch("external_api.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Connection error")

        try:
            _get_exchange_rate("USD", 100.00)
            assert False, "Должно было возникнуть исключение"
        except ValueError as e:
            assert "Ошибка API" in str(e)


def test_no_api_key():
    """Тест отсутствия API ключа"""
    with patch("external_api.api_key", None):
        try:
            _get_exchange_rate("USD", 100.00)
            assert False, "Должно было возникнуть исключение"
        except ValueError as e:
            assert "API ключ не настроен" in str(e)


def test_invalid_amount_format():
    """Тест неверного формата суммы"""
    transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}}

    try:
        convert_to_rub(transaction)
        assert False, "Должно было возникнуть исключение"
    except ValueError as e:
        assert "Ошибка конвертации суммы" in str(e)


if __name__ == "__main__":
    # Запуск всех тестов
    test_rub_transaction()
    test_usd_transaction_success()
    test_eur_transaction_success()
    test_unsupported_currency()
    test_missing_operation_amount()
    test_missing_amount_field()
    test_missing_currency_code()
    test_get_exchange_rate_success()
    test_get_exchange_rate_api_error()
    test_no_api_key()
    test_invalid_amount_format()

    print("✅ Все тесты пройдены успешно!")
