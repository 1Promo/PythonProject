import os
import requests
from dotenv import load_dotenv
from typing import Dict, Union

load_dotenv()


class CurrencyConverter:
    def __init__(self):
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        base_url = "https://api.apilayer.com/exchangerates_data/convert"

        def _get_exchange_rate(currency: str, amount: float) -> float:
            """
            Получает курс обмена указанной валюты на рубли (RUB) через внешний API.
            """
            if not api_key:
                raise ValueError("API ключ не настроен")
            try:
                response = requests.get(
                    base_url,
                    params={"to": "RUB", "from": currency, "amount": amount},
                    headers={"apikey": api_key},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                rate = data["result"]
                return rate
            except requests.RequestException as e:
                raise ValueError(f"Ошибка API: {str(e)}")

        def convert_to_rub(transaction: Dict[str, Union[str, dict]]) -> float:
            """
            Конвертирует сумму транзакции в рубли (RUB), если валюта отличается от RUB.
            """
            try:
                amount_str = transaction["operationAmount"]["amount"]
                currency = transaction["operationAmount"]["currency"]["code"].upper()
                amount = float(amount_str)

                if currency == "RUB":
                    return amount

                if currency not in ("USD", "EUR"):
                    raise ValueError(f"Неподдерживаемая валюта: {currency}")

                return _get_exchange_rate(currency, amount)

            except KeyError as e:
                raise ValueError(f"Неверная структура транзакции: отсутствует поле {e}")
            except ValueError as e:
                raise ValueError(f"Ошибка конвертации суммы: {e}")
