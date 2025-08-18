# Тесты
from conftest import filter_by_currency, invalid_transactions, get_descriptions


def test_filter_usd(mixed_transactions):
    transactions = mixed_transactions
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2, f"Ожидалось 2 USD транзакции, найдено {len(result)}"
    for tx in result:
        assert tx["operationAmount"]["currency"]["code"] == "USD"


def test_filter_rub(mixed_transactions):
    transactions = mixed_transactions
    result = list(filter_by_currency(transactions, "RUB"))
    assert len(result) == 1, f"Ожидалась 1 RUB транзакция, найдено {len(result)}"


def test_filter_invalid():
    transactions = invalid_transactions()
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0, f"Ожидался пустой результат, найдено {len(result)}"


def test_descriptions(mixed_transactions):
    transactions = mixed_transactions
    descriptions = list(get_descriptions(transactions))
    expected = ["Перевод 1", "Перевод 2", "Перевод 3"]
    assert descriptions == expected, f"Описания не совпадают: {descriptions}"
