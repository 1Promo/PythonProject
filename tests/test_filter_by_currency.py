import unittest

from src.filter_by_currency import filter_by_currency


class TestFilterByCurrency(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.transactions = [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100",
                    "currency": {"name": "USD", "code": "USD"}
                }
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200",
                    "currency": {"name": "EUR", "code": "EUR"}
                }
            },
            {
                "id": 3,
                "operationAmount": {
                    "amount": "300",
                    "currency": {"name": "USD", "code": "USD"}
                }
            },
            {
                "id": 4,
                "operationAmount": {
                    "amount": "400",
                    "currency": {"name": "RUB", "code": "RUB"}
                }
            }
        ]

    def test_filter_usd(self):
        # Проверяем фильтрацию по USD
        usd_filter = filter_by_currency(self.transactions, "USD")
        usd_transactions = list(usd_filter)
        self.assertEqual(len(usd_transactions), 2)
        for tx in usd_transactions:
            self.assertEqual(tx['operationAmount']['currency']['code'], 'USD')

    def test_filter_eur(self):
        # Проверяем фильтрацию по EUR
        eur_filter = filter_by_currency(self.transactions, "EUR")
        eur_transactions = list(eur_filter)
        self.assertEqual(len(eur_transactions), 1)
        self.assertEqual(eur_transactions[0]['operationAmount']['currency']['code'], 'EUR')

    def test_filter_nonexistent_currency(self):
        # Проверяем фильтрацию по несуществующей валюте
        nonexistent_filter = filter_by_currency(self.transactions, "GBP")
        result = list(nonexistent_filter)
        self.assertEqual(len(result), 0)

    def test_empty_list(self):
        # Проверяем работу с пустым списком
        empty_filter = filter_by_currency([], "USD")
        result = list(empty_filter)
        self.assertEqual(len(result), 0)

    def test_missing_currency_field(self):
        # Проверяем обработку транзакций без поля currency
        broken_transactions = [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100"
                }
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200",
                    "currency": {"name": "USD", "code": "USD"}
                }
            }
        ]
        filter_result = filter_by_currency(broken_transactions, "USD")
        result = list(filter_result)
        self.assertEqual(len(result), 1)

    def test_invalid_currency_structure(self):
        # Проверяем обработку некорректной структуры
        invalid_transactions = [
            {
                "id": 1,
                "operationAmount": "invalid_data"
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200",
                    "currency": {"name": "USD", "code": "USD"}
                }
            }
        ]
        filter_result = filter_by_currency(invalid_transactions, "USD")
        result = list(filter_result)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
