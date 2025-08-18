def filter_by_currency(transactions, target_currency):
    """
    Фильтрует транзакции по указанной валюте.

    Параметры:
    transactions (list): список словарей с транзакциями
    target_currency (str): код валюты для фильтрации (например, "USD")

    Возвращает:
    iterator: итератор, возвращающий транзакции с указанной валютой
    """
    for transaction in transactions:
        try:
            # Проверяем структуру вложенных словарей
            currency_info = transaction.get('operationAmount', {}).get('currency', {})
            currency_code = currency_info.get('code')

            # Сравниваем код валюты с целевым значением
            if currency_code == target_currency:
                yield transaction

        except AttributeError:
            # Обработка ошибок в структуре данных
            continue


# Пример данных для тестирования
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2020-01-01T00:00:00",
        "operationAmount": {
            "amount": "1000",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 12345678901234567890",
        "to": "Счет 98765432109876543210"
    }
]

# Создаем итератор для USD транзакций
usd_transactions = filter_by_currency(transactions, "USD")

# Пример вывода первых двух транзакций
for _ in range(2):
    print(next(usd_transactions))
