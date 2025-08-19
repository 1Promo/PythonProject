import os
import requests
from dotenv import load_dotenv
from typing import Dict, Union

load_dotenv()


class CurrencyConverter:
    def __init__(self):
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.base_url = "https://api.apilayer.com/exchangerates_data/convert"
        self.cache = {}  # Кэш курсов валют

    def convert_to_rub(self, transaction: Dict[str, Union[str, dict]]) -> float:
        """
        Конвертирует сумму транзакции в рубли.

        Args:
            transaction: Словарь с данными о транзакции, должен содержать:
                - operationAmount.amount (str/float): сумма
                - operationAmount.currency.code (str): код валюты (RUB, USD, EUR)

        Returns:
            Сумма в рублях (float)

        Raises:
            ValueError: При ошибках валидации или API
        """
        try:
            # Извлекаем данные из транзакции
            amount_str = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["code"].upper()
            amount = float(amount_str)

            # Если валюта уже в рублях
            if currency == "RUB":
                return amount

            # Проверка поддерживаемых валют
            if currency not in ("USD", "EUR"):
                raise ValueError(f"Неподдерживаемая валюта: {currency}")

            # Получаем курс
            rate = self._get_exchange_rate(currency)
            return round(amount * rate, 2)

        except KeyError as e:
            raise ValueError(f"Неверная структура транзакции: отсутствует поле {e}")
        except ValueError as e:
            raise ValueError(f"Ошибка конвертации суммы: {e}")

    def _get_exchange_rate(self, currency: str) -> float:
        """Получает курс валюты к рублю с кэшированием."""
        if currency in self.cache:
            return self.cache[currency]

        if not self.api_key:
            raise ValueError("API ключ не настроен")

        try:
            response = requests.get(
                self.base_url,
                params={"base": currency, "symbols": "RUB"},
                headers={"apikey": self.api_key},
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            rate = data["rates"]["RUB"]
            self.cache[currency] = rate  # Кэшируем курс
            return rate

        except requests.RequestException as e:
            raise ValueError(f"Ошибка API: {str(e)}")
