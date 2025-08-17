import os
import requests
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict) -> float:
    """Конвертирует сумму транзакции в рубли по текущему курсу.

    Для транзакций в RUB возвращает сумму без конвертации.
    Для USD и EUR выполняет конвертацию через внешнее API.

    Args:
        transaction: Словарь с данными о транзакции, должен содержать
            'operationAmount' с полями 'amount' и 'currency' (с кодом валюты)

    Returns:
        Сумма транзакции в рублях (float)

    Raises:
        ValueError: Если валюта не поддерживается, отсутствует API ключ или
            возникла ошибка при запросе к API

    Examples:
        >>> transaction = {
        ...     'operationAmount': {
        ...         'amount': '100.0',
        ...         'currency': {'code': 'RUB'}
        ...     }
        ... }
        >>> convert_to_rub(transaction)
        100.0

        >>> transaction = {
        ...     'operationAmount': {
        ...         'amount': '10.0',
        ...         'currency': {'code': 'USD'}
        ...     }
        ... }
        >>> convert_to_rub(transaction)  # При курсе 90.5 RUB/USD
        905.0
    """
    try:
        operation_amount = transaction["operationAmount"]
        amount = float(operation_amount["amount"])
        currency = operation_amount["currency"]["code"].upper()

        if currency == "RUB":
            return amount

        if currency not in ("USD", "EUR"):
            raise ValueError(f"Unsupported currency: {currency}")

        if not API_KEY:
            raise ValueError("API key not configured")

        response = requests.get(
            BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=10
        )

        if not response.ok:
            raise ValueError(f"API request failed: {response.text}")

        rate = response.json()["rates"]["RUB"]
        return amount * rate

    except KeyError as e:
        raise ValueError(f"Invalid transaction structure: missing {e}")
    except ValueError as e:
        raise ValueError(f"Invalid amount value: {e}")
